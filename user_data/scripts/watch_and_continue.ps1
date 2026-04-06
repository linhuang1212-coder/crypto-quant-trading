#Requires -Version 5.1
<#
.SYNOPSIS
    Watches for the first batch to finish, then runs remaining experiments.
    This script monitors the old runner's progress and starts run_all_experiments.ps1
    when it detects the first batch has completed.
#>

$ErrorActionPreference = "Continue"
$workDir = "c:\Users\hlin2\freqtrade"
Set-Location $workDir

$resultsCsv = "user_data/experiment_results/all_results.csv"

Write-Host "Watching for first batch (112 experiments) to complete..."
Write-Host "Will auto-start remaining ~280 experiments when done."
Write-Host ""

$lastCount = 0
$stableCount = 0

while ($true) {
    Start-Sleep -Seconds 30

    if (Test-Path $resultsCsv) {
        $lineCount = (Get-Content $resultsCsv | Measure-Object -Line).Lines - 1
    } else {
        $lineCount = 0
    }

    if ($lineCount -ne $lastCount) {
        Write-Host "  Progress: $lineCount / 112 experiments done ($(Get-Date -Format 'HH:mm:ss'))"
        $lastCount = $lineCount
        $stableCount = 0
    } else {
        $stableCount++
    }

    # If we have 100+ results and no new ones for 5 minutes, the first batch is done
    if ($lineCount -ge 100 -and $stableCount -ge 10) {
        Write-Host ""
        Write-Host "First batch appears complete ($lineCount experiments done)." -ForegroundColor Green
        Write-Host "Starting remaining experiments..." -ForegroundColor Cyan
        Write-Host ""
        break
    }

    # Also break if all 112 are done
    if ($lineCount -ge 112) {
        Write-Host ""
        Write-Host "All 112 first-batch experiments completed!" -ForegroundColor Green
        Write-Host "Starting remaining experiments..." -ForegroundColor Cyan
        Write-Host ""
        break
    }
}

# Now run the smart-resume script which skips already-completed experiments
& powershell -ExecutionPolicy Bypass -File "$workDir\user_data\scripts\run_all_experiments.ps1"
