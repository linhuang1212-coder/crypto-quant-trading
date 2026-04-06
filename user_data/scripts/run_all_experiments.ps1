#Requires -Version 5.1
<#
.SYNOPSIS
    8-Hour Automated Experiment Runner (Smart Resume)
    Runs all experiments from manifest, skipping already-completed ones.
    Expected runtime: 5-8 hours for 392 experiments.

.USAGE
    powershell -ExecutionPolicy Bypass -File user_data/scripts/run_all_experiments.ps1
#>

$ErrorActionPreference = "Continue"
$startTime = Get-Date
$workDir = "c:\Users\hlin2\freqtrade"
Set-Location $workDir

$manifestPath = "user_data/experiment_manifest.json"
$resultsDir = "user_data/experiment_results"
$resultsCsv = "$resultsDir/all_results.csv"
$progressFile = "$resultsDir/progress.txt"
$configBase = "user_data/config_backtest.json"

if (-not (Test-Path $resultsDir)) { New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null }

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$total = $manifest.Count

# Check which experiments are already done
$completedStrategies = @{}
if (Test-Path $resultsCsv) {
    $existingLines = Get-Content $resultsCsv | Select-Object -Skip 1
    foreach ($line in $existingLines) {
        if ($line -match "^([^,]+),") {
            $completedStrategies[$Matches[1]] = $true
        }
    }
    Write-Host "Found $($completedStrategies.Count) already-completed experiments, will skip them." -ForegroundColor Yellow
} else {
    "strategy,group,name,trades,avg_profit_pct,tot_profit_usdt,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,avg_duration,cagr,sortino,params" | Out-File $resultsCsv -Encoding utf8
}

$remaining = @()
foreach ($exp in $manifest) {
    if (-not $completedStrategies.ContainsKey($exp.strategy)) {
        $remaining += $exp
    }
}

$totalRemaining = $remaining.Count

Write-Host "=============================================="
Write-Host " 8-Hour Experiment Runner (Smart Resume)"
Write-Host " Total in manifest: $total"
Write-Host " Already completed: $($completedStrategies.Count)"
Write-Host " Remaining: $totalRemaining"
Write-Host " Started: $startTime"
Write-Host " Est. finish: $($startTime.AddMinutes($totalRemaining * 0.9))"
Write-Host "=============================================="
Write-Host ""

$completed = 0
$failed = 0
$strategyDir = "/freqtrade/user_data/strategies/experiments"

for ($i = 0; $i -lt $totalRemaining; $i++) {
    $exp = $remaining[$i]
    $strategy = $exp.strategy
    $group = $exp.group
    $name = $exp.name
    $paramsJson = ($exp.params | ConvertTo-Json -Compress) -replace '"', '""'

    $elapsed = (Get-Date) - $startTime
    $globalIdx = $completedStrategies.Count + $i + 1
    $pct = if ($total -gt 0) { [math]::Round(($globalIdx / $total) * 100, 1) } else { 0 }
    $etaMin = if ($i -gt 0) { [math]::Round(($elapsed.TotalMinutes / $i) * ($totalRemaining - $i), 0) } else { "?" }

    Write-Host "[$globalIdx/$total] ($pct%) $group :: $name  (ETA: ${etaMin}min)" -ForegroundColor Cyan
    "$((Get-Date).ToString('HH:mm:ss')) [$globalIdx/$total] $strategy - $name" | Out-File $progressFile -Append -Encoding utf8

    try {
        $rawOutput = docker run --rm `
            -v "./user_data:/freqtrade/user_data" `
            freqtradeorg/freqtrade:stable backtesting `
            --config /freqtrade/user_data/config_backtest.json `
            --strategy $strategy `
            --strategy-path $strategyDir `
            --timerange 20200101-20260401 `
            --cache none `
            --starting-balance 1000 2>&1

        $trades = "0"; $totProfitPct = "0"; $totProfitUsdt = "0"
        $sharpe = "0"; $pf = "0"; $maxDD = "0"; $cagr = "0"; $sortino = "0"; $winRate = "0"
        $avgProfit = "0"

        foreach ($line in ($rawOutput | ForEach-Object { $_.ToString() })) {
            if ($line -match "Total/Daily Avg Trades\s+.+\s+(\d+)\s+/") { $trades = $Matches[1] }
            if ($line -match "Total profit %\s+.+\s+([\-\d\.]+)%") { $totProfitPct = $Matches[1] }
            if ($line -match "Absolute profit\s+.+\s+([\-\d\.]+)\s+USDT") { $totProfitUsdt = $Matches[1] }
            if ($line -match "Sharpe\s+.+\s+([\-\d\.]+)") { $sharpe = $Matches[1] }
            if ($line -match "Sortino\s+.+\s+([\-\d\.]+)") { $sortino = $Matches[1] }
            if ($line -match "Profit factor\s+.+\s+([\-\d\.]+)") { $pf = $Matches[1] }
            if ($line -match "CAGR %\s+.+\s+([\-\d\.]+)") { $cagr = $Matches[1] }
            if ($line -match "Absolute drawdown\s+.+\(([\d\.]+)%\)") { $maxDD = $Matches[1] }
            if ($line -match "TOTAL.*\s+(\d+)\s+0\s+(\d+)\s+([\d\.]+)") { $winRate = $Matches[3] }
        }

        if ([int]$trades -gt 0 -and [double]$totProfitPct -ne 0) {
            $avgProfit = [math]::Round([double]$totProfitPct / [int]$trades, 2)
        }

        "$strategy,$group,`"$name`",$trades,$avgProfit,$totProfitUsdt,$totProfitPct,$sharpe,$pf,$maxDD,$winRate,0,$cagr,$sortino,`"$paramsJson`"" | Out-File $resultsCsv -Append -Encoding utf8

        $color = if ([double]$sharpe -gt 0.5) { "Green" } elseif ([double]$sharpe -gt 0) { "Yellow" } else { "Red" }
        Write-Host "  -> Trades=$trades  Sharpe=$sharpe  PF=$pf  Profit=${totProfitPct}%  DD=${maxDD}%" -ForegroundColor $color

        $completed++

        if ([double]$sharpe -ge 0.6) {
            $rawText = $rawOutput -join "`n"
            $rawText | Out-File "$resultsDir/${strategy}_raw.txt" -Encoding utf8
        }
    }
    catch {
        Write-Host "  -> FAILED: $_" -ForegroundColor Red
        "$strategy,$group,`"$name`",FAILED,,,,,,,,,,`"$paramsJson`"" | Out-File $resultsCsv -Append -Encoding utf8
        $failed++
    }
}

$endTime = Get-Date
$totalElapsed = $endTime - $startTime

Write-Host ""
Write-Host "=============================================="
Write-Host " EXPERIMENT RUN COMPLETE"
Write-Host " New: $completed  |  Failed: $failed  |  Previously done: $($completedStrategies.Count)"
Write-Host " Grand total: $($completedStrategies.Count + $completed)"
Write-Host " Duration: $($totalElapsed.ToString('hh\:mm\:ss'))"
Write-Host " Results: $resultsCsv"
Write-Host "=============================================="

$summaryPath = "$resultsDir/summary.txt"
@"
Experiment Run Summary
======================
Start: $startTime
End:   $endTime
Duration: $($totalElapsed.ToString('hh\:mm\:ss'))
Total in manifest: $total
Previously completed: $($completedStrategies.Count)
Newly completed: $completed
Failed: $failed
Grand total completed: $($completedStrategies.Count + $completed)
Results CSV: $resultsCsv

Run: python user_data/scripts/analyze_results.py
"@ | Out-File $summaryPath -Encoding utf8

Write-Host ""
Write-Host "Run: python user_data/scripts/analyze_results.py" -ForegroundColor Yellow
