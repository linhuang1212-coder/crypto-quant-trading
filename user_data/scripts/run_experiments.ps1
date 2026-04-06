#Requires -Version 5.1
<#
.SYNOPSIS
    8-Hour Automated Experiment Runner
    Runs 112+ backtests automatically, saves results to CSV.
    Expected runtime: 6-8 hours.

.USAGE
    powershell -ExecutionPolicy Bypass -File user_data/scripts/run_experiments.ps1
#>

$ErrorActionPreference = "Continue"
$startTime = Get-Date
$workDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $workDir

$manifestPath = "user_data/experiment_manifest.json"
$resultsDir = "user_data/experiment_results"
$resultsCsv = "$resultsDir/all_results.csv"
$progressFile = "$resultsDir/progress.txt"
$configBase = "user_data/config_backtest.json"

if (-not (Test-Path $resultsDir)) { New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null }

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$total = $manifest.Count

# Write CSV header
"strategy,group,name,trades,avg_profit_pct,tot_profit_usdt,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,avg_duration,cagr,sortino,params" | Out-File $resultsCsv -Encoding utf8

Write-Host "=============================================="
Write-Host " 8-Hour Experiment Runner"
Write-Host " Total experiments: $total"
Write-Host " Started: $startTime"
Write-Host " Estimated finish: $($startTime.AddHours(8))"
Write-Host "=============================================="
Write-Host ""

$completed = 0
$failed = 0

for ($i = 0; $i -lt $total; $i++) {
    $exp = $manifest[$i]
    $strategy = $exp.strategy
    $group = $exp.group
    $name = $exp.name
    $paramsJson = ($exp.params | ConvertTo-Json -Compress) -replace '"', '""'

    $elapsed = (Get-Date) - $startTime
    $pct = if ($total -gt 0) { [math]::Round(($i / $total) * 100, 1) } else { 0 }
    $etaMin = if ($i -gt 0) { [math]::Round(($elapsed.TotalMinutes / $i) * ($total - $i), 0) } else { "?" }

    Write-Host "[$($i+1)/$total] ($pct%) $group :: $name  (ETA: ${etaMin}min remaining)" -ForegroundColor Cyan
    "$((Get-Date).ToString('HH:mm:ss')) [$($i+1)/$total] $strategy - $name" | Out-File $progressFile -Append -Encoding utf8

    $strategyDir = "/freqtrade/user_data/strategies/experiments"
    $rawOutput = ""

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

        $rawText = $rawOutput -join "`n"

        $trades = "0"
        $avgProfit = "0"
        $totProfitUsdt = "0"
        $totProfitPct = "0"
        $sharpe = "0"
        $pf = "0"
        $maxDD = "0"
        $winRate = "0"
        $avgDuration = "0"
        $cagr = "0"
        $sortino = "0"

        foreach ($line in ($rawOutput | ForEach-Object { $_.ToString() })) {
            # SUMMARY METRICS section - more reliable than table parsing
            if ($line -match "Total/Daily Avg Trades\s+.+\s+(\d+)\s+/") {
                $trades = $Matches[1]
            }
            if ($line -match "Total profit %\s+.+\s+([\-\d\.]+)%") {
                $totProfitPct = $Matches[1]
            }
            if ($line -match "Absolute profit\s+.+\s+([\-\d\.]+)\s+USDT") {
                $totProfitUsdt = $Matches[1]
            }
            if ($line -match "Sharpe\s+.+\s+([\-\d\.]+)") {
                $sharpe = $Matches[1]
            }
            if ($line -match "Sortino\s+.+\s+([\-\d\.]+)") {
                $sortino = $Matches[1]
            }
            if ($line -match "Profit factor\s+.+\s+([\-\d\.]+)") {
                $pf = $Matches[1]
            }
            if ($line -match "CAGR %\s+.+\s+([\-\d\.]+)") {
                $cagr = $Matches[1]
            }
            if ($line -match "Absolute drawdown\s+.+\(([\d\.]+)%\)") {
                $maxDD = $Matches[1]
            }
            # Parse win rate from STRATEGY SUMMARY line (last TOTAL line with win%)
            if ($line -match "TOTAL.*\s+(\d+)\s+0\s+(\d+)\s+([\d\.]+)") {
                $winRate = $Matches[3]
            }
        }

        # Calculate avg profit if we have trades and total
        if ([int]$trades -gt 0 -and [double]$totProfitPct -ne 0) {
            $avgProfit = [math]::Round([double]$totProfitPct / [int]$trades, 2)
        }

        "$strategy,$group,`"$name`",$trades,$avgProfit,$totProfitUsdt,$totProfitPct,$sharpe,$pf,$maxDD,$winRate,$avgDuration,$cagr,$sortino,`"$paramsJson`"" | Out-File $resultsCsv -Append -Encoding utf8

        $color = if ([double]$sharpe -gt 0.5) { "Green" } elseif ([double]$sharpe -gt 0) { "Yellow" } else { "Red" }
        Write-Host "  -> Trades=$trades  Sharpe=$sharpe  PF=$pf  Profit=${totProfitPct}%  DD=${maxDD}%" -ForegroundColor $color

        $completed++

        # Save raw output for top performers
        if ([double]$sharpe -ge 0.5) {
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
Write-Host " Total: $total  |  Success: $completed  |  Failed: $failed"
Write-Host " Duration: $($totalElapsed.ToString('hh\:mm\:ss'))"
Write-Host " Results: $resultsCsv"
Write-Host "=============================================="

# Generate summary
$summaryPath = "$resultsDir/summary.txt"
@"
Experiment Run Summary
======================
Start: $startTime
End:   $endTime
Duration: $($totalElapsed.ToString('hh\:mm\:ss'))
Total: $total  |  Success: $completed  |  Failed: $failed
Results CSV: $resultsCsv

Run analyze_results.py to generate the full analysis report.
"@ | Out-File $summaryPath -Encoding utf8

Write-Host ""
Write-Host "Now run: python user_data/scripts/analyze_results.py" -ForegroundColor Yellow
