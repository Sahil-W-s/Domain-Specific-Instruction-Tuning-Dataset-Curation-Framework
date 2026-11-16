param(
    [int]$BatchSize = 50,
    [int]$MaxBatches = 0,
    [switch]$PreflightOnly
)

$ErrorActionPreference = "Stop"
$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

$RegistryPath = Join-Path $ProjectRoot "manifests\artifact_registry.jsonl"
$ConfigPath = Join-Path $ProjectRoot ".local\source_roots.local.yml"
$HashScript = Join-Path $ProjectRoot "scripts\hash_artifacts_resumable.py"
$Reconciler = Join-Path $ProjectRoot "scripts\reconcile_failed_artifacts.py"
$CheckpointPath = Join-Path $ProjectRoot "state\hash_progress.json"
$EventsPath = Join-Path $ProjectRoot "reports\inventory\hash_batches\hash_events.jsonl"

function Read-Registry {
    $records = @(
        Get-Content -LiteralPath $RegistryPath |
        Where-Object { $_.Trim() } |
        ForEach-Object { $_ | ConvertFrom-Json }
    )

    $ids = @($records | ForEach-Object { $_.artifact_id })
    if ($ids.Count -ne @($ids | Select-Object -Unique).Count) {
        throw "Duplicate artifact IDs detected."
    }

    return ,$records
}

function Get-Counts($records) {
    $counts = @{
        verified = 0
        pending = 0
        failed = 0
        not_applicable = 0
    }

    foreach ($r in $records) {
        if (-not $counts.ContainsKey([string]$r.hash_status)) {
            throw "Unexpected hash status: $($r.hash_status)"
        }
        $counts[[string]$r.hash_status]++
    }

    return $counts
}

function Get-UnresolvedFailures($records) {
    $byId = @{}
    foreach ($r in $records) { $byId[$r.artifact_id] = $r }

    $unresolved = @()

    foreach ($failure in ($records | Where-Object { $_.hash_status -eq "failed" })) {
        if ($failure.notes -notmatch "Superseded") {
            $unresolved += $failure
            continue
        }

        if ($failure.notes -notmatch "(art-[0-9a-f]{16})") {
            throw "Superseded record has no replacement ID: $($failure.artifact_id)"
        }

        $replacementId = $Matches[1]
        if (-not $byId.ContainsKey($replacementId)) {
            throw "Replacement record missing: $replacementId"
        }

        if ($byId[$replacementId].hash_status -notin @("pending", "verified")) {
            throw "Replacement has invalid status: $replacementId"
        }
    }

    return ,$unresolved
}

function Read-EventCount {
    if (-not (Test-Path -LiteralPath $EventsPath)) { return 0 }
    return @(Get-Content -LiteralPath $EventsPath |
        Where-Object { $_.Trim() }).Count
}

if ($BatchSize -lt 1 -or $BatchSize -gt 50) {
    throw "BatchSize must be between 1 and 50."
}

foreach ($required in @(
    $RegistryPath, $ConfigPath, $HashScript, $Reconciler, $EventsPath
)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Required file missing: $required"
    }
}

Write-Host "`n========== PHASE 2 AUTOMATIC RECONCILIATION ==========" -ForegroundColor Cyan

& python $Reconciler --dry-run
if ($LASTEXITCODE -ne 0) {
    throw "Reconciliation dry-run failed. No hashing started."
}

$records = Read-Registry
$counts = Get-Counts $records
$unresolved = Get-UnresolvedFailures $records

if ($unresolved.Count -gt 0) {
    throw "Unresolved failures remain after dry-run."
}

Write-Host "`n========== PREFLIGHT ==========" -ForegroundColor Cyan
Write-Host "Registry records: $($records.Count)"
Write-Host "Verified: $($counts.verified)"
Write-Host "Pending: $($counts.pending)"
Write-Host "Historical failures: $($counts.failed)"
Write-Host "Not applicable: $($counts.not_applicable)"
Write-Host "Batch size: $BatchSize"

if ($PreflightOnly) {
    Write-Host "`nPREFLIGHT PASSED. No registry changes or hashing performed." -ForegroundColor Green
    return
}

$logDir = Join-Path $ProjectRoot "reports\inventory\phase2_controller_runs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logPath = Join-Path $logDir "controller_$stamp.log"

Start-Transcript -Path $logPath -Force | Out-Null

try {
    $batchNumber = 0

    while ($true) {
        if ($MaxBatches -gt 0 -and $batchNumber -ge $MaxBatches) {
            Write-Host "Maximum batch limit reached. Checkpoint retained."
            break
        }

        # Reconcile before every batch.
        Write-Host "`n========== AUTOMATIC RECONCILIATION ==========" -ForegroundColor Cyan
        & python $Reconciler

        if ($LASTEXITCODE -ne 0) {
            throw "Automatic reconciliation blocked. Review unresolved failures."
        }

        $recordsBefore = Read-Registry
        $beforeCounts = Get-Counts $recordsBefore
        $unresolved = Get-UnresolvedFailures $recordsBefore

        if ($unresolved.Count -gt 0) {
            throw "Unresolved failures remain. Stopping safely."
        }

        if ($beforeCounts.pending -eq 0) {
            Write-Host "All pending hashes completed." -ForegroundColor Green
            break
        }

        $batchNumber++
        $eventsBefore = Read-EventCount
        $pendingBefore = $beforeCounts.pending

        Write-Host "`n========== BATCH $batchNumber ==========" -ForegroundColor Cyan
        Write-Host "Pending before batch: $pendingBefore"

        & python $HashScript --batch-size $BatchSize

        if ($LASTEXITCODE -ne 0) {
            throw "Hashing script exited with code $LASTEXITCODE."
        }

        $recordsAfter = Read-Registry
        $afterCounts = Get-Counts $recordsAfter

        $processed = $pendingBefore - $afterCounts.pending
        if ($processed -le 0) {
            throw "No pending records processed. Stopping."
        }

        $eventsAfter = Read-EventCount
        if (($eventsAfter - $eventsBefore) -ne $processed) {
            throw "Event log delta does not match processed records."
        }

        if (-not (Test-Path -LiteralPath $CheckpointPath)) {
            throw "Checkpoint missing."
        }

        $checkpoint = Get-Content -LiteralPath $CheckpointPath -Raw |
            ConvertFrom-Json

        foreach ($status in @("verified", "pending", "failed", "not_applicable")) {
            if ([int]$checkpoint.registry_status_counts.$status -ne
                [int]$afterCounts[$status]) {
                throw "Checkpoint mismatch for status: $status"
            }
        }

        Write-Host "`nBATCH VALIDATION PASSED" -ForegroundColor Green
        Write-Host "Processed: $processed"
        Write-Host "Verified: $($afterCounts.verified)"
        Write-Host "Pending: $($afterCounts.pending)"
        Write-Host "Failed: $($afterCounts.failed)"
        Write-Host "Not applicable: $($afterCounts.not_applicable)"
        Write-Host "Event delta: $($eventsAfter - $eventsBefore)"
    }

    $finalRecords = Read-Registry
    $finalCounts = Get-Counts $finalRecords

    Write-Host "`n========== FINAL CONTROLLER STATUS ==========" -ForegroundColor Cyan
    $finalCounts.GetEnumerator() | Sort-Object Name |
        Format-Table Name, Value -AutoSize

    Write-Host "Total records: $($finalRecords.Count)"
    Write-Host "Controller log: $logPath"

    if ($finalCounts.pending -eq 0) {
        Write-Host "HASHING STAGE COMPLETE." -ForegroundColor Green
    }
    else {
        Write-Host "HASHING STAGE PAUSED. Rerun the same command to resume."
    }
}
finally {
    Stop-Transcript | Out-Null
}
