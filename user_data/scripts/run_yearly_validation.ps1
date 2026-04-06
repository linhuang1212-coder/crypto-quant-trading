#Requires -Version 5.1
<#
.SYNOPSIS
    分年度验证脚本 — 对 4 个候选策略做 6 段年度回测
    候选A: Exp_TrailPos_003 (TrailPos=0.03)
    候选B: V3_NB_ATR06 (TrailPos=0.03 + ATR=0.6)
    候选C: V3_NB_DC14 (TrailPos=0.03 + DC=14)
    候选D: V3_Vol_50_20 (Vol>2.0x, 50期均量)
    基线:  CryptoV10 (当前实盘)
#>

$ErrorActionPreference = "Continue"
$startTime = Get-Date
$workDir = "c:\Users\hlin2\freqtrade"
Set-Location $workDir

$resultsDir = "user_data/experiment_results"
$resultsCsv = "$resultsDir/yearly_validation.csv"

"strategy,label,year,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino" | Out-File $resultsCsv -Encoding utf8

$strategies = @(
    @{strategy="CryptoV10"; label="Baseline"; path="/freqtrade/user_data/strategies"},
    @{strategy="Exp_TrailPos_003"; label="A_TrailPos003"; path="/freqtrade/user_data/strategies/experiments"},
    @{strategy="V3_NB_ATR06"; label="B_NB_ATR06"; path="/freqtrade/user_data/strategies/experiments"},
    @{strategy="V3_NB_DC14"; label="C_NB_DC14"; path="/freqtrade/user_data/strategies/experiments"},
    @{strategy="V3_Vol_50_20"; label="D_Vol50_2x"; path="/freqtrade/user_data/strategies/experiments"}
)

$periods = @(
    @{year="2020"; range="20200101-20210101"},
    @{year="2021"; range="20210101-20220101"},
    @{year="2022"; range="20220101-20230101"},
    @{year="2023"; range="20230101-20240101"},
    @{year="2024"; range="20240101-20250101"},
    @{year="2025-Q1"; range="20250101-20260401"}
)

$total = $strategies.Count * $periods.Count
$done = 0

Write-Host "=============================================="
Write-Host " Yearly Validation: $($strategies.Count) strategies x $($periods.Count) periods = $total runs"
Write-Host " Started: $startTime"
Write-Host "=============================================="

foreach ($strat in $strategies) {
    foreach ($period in $periods) {
        $done++
        $pct = [math]::Round(($done / $total) * 100, 0)
        Write-Host "[$done/$total] ($pct%) $($strat.label) / $($period.year)" -ForegroundColor Cyan

        $rawOutput = docker run --rm `
            -v "./user_data:/freqtrade/user_data" `
            freqtradeorg/freqtrade:stable backtesting `
            --config /freqtrade/user_data/config_backtest.json `
            --strategy $($strat.strategy) `
            --strategy-path $($strat.path) `
            --timerange $($period.range) `
            --cache none `
            --starting-balance 1000 2>&1

        $trades = "0"; $totProfitPct = "0"; $sharpe = "0"; $pf = "0"
        $maxDD = "0"; $cagr = "0"; $sortino = "0"; $winRate = "0"

        foreach ($line in ($rawOutput | ForEach-Object { $_.ToString() })) {
            if ($line -match "Total/Daily Avg Trades\s+.+\s+(\d+)\s+/") { $trades = $Matches[1] }
            if ($line -match "Total profit %\s+.+\s+([\-\d\.]+)%") { $totProfitPct = $Matches[1] }
            if ($line -match "Sharpe\s+.+\s+([\-\d\.]+)") { $sharpe = $Matches[1] }
            if ($line -match "Sortino\s+.+\s+([\-\d\.]+)") { $sortino = $Matches[1] }
            if ($line -match "Profit factor\s+.+\s+([\-\d\.]+)") { $pf = $Matches[1] }
            if ($line -match "CAGR %\s+.+\s+([\-\d\.]+)") { $cagr = $Matches[1] }
            if ($line -match "Absolute drawdown\s+.+\(([\d\.]+)%\)") { $maxDD = $Matches[1] }
            if ($line -match "TOTAL.*\s+(\d+)\s+0\s+(\d+)\s+([\d\.]+)") { $winRate = $Matches[3] }
        }

        $color = if ([double]$sharpe -gt 0.5) { "Green" } elseif ([double]$sharpe -gt 0) { "Yellow" } else { "Red" }
        Write-Host "  -> Trades=$trades Sharpe=$sharpe PF=$pf Profit=${totProfitPct}% DD=${maxDD}%" -ForegroundColor $color

        "$($strat.strategy),$($strat.label),$($period.year),$($period.range),$trades,$totProfitPct,$sharpe,$pf,$maxDD,$winRate,$cagr,$sortino" | Out-File $resultsCsv -Append -Encoding utf8
    }
}

$endTime = Get-Date
Write-Host ""
Write-Host "=============================================="
Write-Host " DONE in $((($endTime - $startTime).TotalMinutes.ToString('0.0'))) minutes"
Write-Host " Results: $resultsCsv"
Write-Host "=============================================="
