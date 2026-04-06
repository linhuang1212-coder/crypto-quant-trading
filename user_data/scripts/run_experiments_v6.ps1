#Requires -Version 5.1
<#
.SYNOPSIS
    V6 实验流水线：三阶段防过拟合（全样本→年度→WF）→ 分析
.DESCRIPTION
    基于 V5 流水线修复版。不需要下载新数据（使用已有4币种）。
    修复 V5 bug：分年度回测正确传递 strategy-path。
#>

$ErrorActionPreference = "Continue"
$pipelineStart = Get-Date

$workDir = "c:\Users\hlin2\freqtrade"
$DockerImage = "freqtradeorg/freqtrade:stable"
$StrategyPathDocker = "/freqtrade/user_data/strategies/experiments_v6"
$DefaultConfigDocker = "/freqtrade/user_data/config_backtest.json"

Set-Location $workDir

$manifestPath = "user_data/experiment_manifest_v6.json"
$resultsDir = "user_data/experiment_results"
$resultsCsv = "$resultsDir/v6_results.csv"
$yearlyCsv = "$resultsDir/v6_yearly.csv"
$wfCsv = "$resultsDir/v6_walkforward.csv"
$progressFile = "$resultsDir/v6_progress.txt"
$summaryFile = "$resultsDir/v6_pipeline_summary.txt"

# --- helpers ---
function Write-PhaseBanner([string]$Title) {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Magenta
    Write-Host " $Title" -ForegroundColor Magenta
    Write-Host ("=" * 60) -ForegroundColor Magenta
    Write-Host ""
}

function Write-Log([string]$Msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$ts] $Msg" -ForegroundColor Gray
}

function Parse-BacktestOutput([object[]]$rawOutput) {
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
        if ($line -match "Avg profit\s+.+\s+([\-\d\.]+)%") { $avgProfit = $Matches[1] }
    }
    return @{
        trades         = $trades
        totProfitPct   = $totProfitPct
        totProfitUsdt  = $totProfitUsdt
        sharpe         = $sharpe
        pf             = $pf
        maxDD          = $maxDD
        cagr           = $cagr
        sortino        = $sortino
        winRate        = $winRate
        avgProfit      = $avgProfit
    }
}

function Invoke-Backtest {
    param(
        [string]$Strategy,
        [string]$Timerange,
        [string]$ConfigDocker = $DefaultConfigDocker,
        [string]$StrategyPath = $StrategyPathDocker
    )
    $raw = docker run --rm `
        -v "./user_data:/freqtrade/user_data" `
        $DockerImage backtesting `
        --config $ConfigDocker `
        --strategy $Strategy `
        --strategy-path $StrategyPath `
        --timerange $Timerange `
        --cache none `
        --starting-balance 1000 2>&1
    return $raw
}

# --- Load gates config ---
$gatesJsonPath = "user_data/configs/experiment_gates.json"
if (-not (Test-Path $gatesJsonPath)) {
    Write-Host "FATAL: Gates config not found: $gatesJsonPath" -ForegroundColor Red
    exit 1
}
$gates = Get-Content $gatesJsonPath -Raw | ConvertFrom-Json
$fullSampleRange = $gates.full_sample_timerange

if (-not (Test-Path $resultsDir)) { New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null }

# --- Load manifest ---
if (-not (Test-Path $manifestPath)) {
    Write-Host "FATAL: Manifest not found: $manifestPath" -ForegroundColor Red
    exit 1
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$manifestByStrategy = @{}
foreach ($e in $manifest) { $manifestByStrategy[$e.strategy] = $e }

# ========== Stage 1 — Full-sample screen ==========
Write-PhaseBanner "STAGE 1 — Full-sample screen ($fullSampleRange)"

$stage1Start = Get-Date
$s1Completed = 0
$s1Failed = 0

$completedStrategies = @{}
if (Test-Path $resultsCsv) {
    $existingLines = Get-Content $resultsCsv -ErrorAction SilentlyContinue | Select-Object -Skip 1
    foreach ($line in $existingLines) {
        if ($line -match "^([^,]+),") { $completedStrategies[$Matches[1]] = $true }
    }
    Write-Host "Resume: $($completedStrategies.Count) strategies already in v6_results.csv" -ForegroundColor Yellow
}
else {
    "strategy,group,name,trades,avg_profit_pct,tot_profit_usdt,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino,params" | Out-File $resultsCsv -Encoding utf8
}

$total = $manifest.Count
$remaining = @()
foreach ($exp in $manifest) {
    if (-not $completedStrategies.ContainsKey($exp.strategy)) { $remaining += $exp }
}
$totalRemaining = $remaining.Count
Write-Host "Manifest: $total | Remaining: $totalRemaining" -ForegroundColor Cyan

for ($i = 0; $i -lt $totalRemaining; $i++) {
    $exp = $remaining[$i]
    $strategy = $exp.strategy
    $group = $exp.group
    $name = $exp.name
    $paramsObj = $exp.params
    if ($null -eq $paramsObj) { $paramsObj = @{} }
    $paramsJson = ($paramsObj | ConvertTo-Json -Compress -Depth 10) -replace '"', '""'

    $elapsed = (Get-Date) - $stage1Start
    $globalIdx = $completedStrategies.Count + $i + 1
    $pct = if ($total -gt 0) { [math]::Round(($globalIdx / $total) * 100, 1) } else { 0 }
    $etaMin = if ($i -gt 0) { [math]::Round(($elapsed.TotalMinutes / $i) * ($totalRemaining - $i), 0) } else { "?" }

    Write-Host "[$globalIdx/$total] ($pct%) $group :: $name  ETA:~${etaMin}min" -ForegroundColor Cyan
    "$(Get-Date -Format 'HH:mm:ss') [S1 $globalIdx/$total] $strategy - $name" | Out-File $progressFile -Append -Encoding utf8

    try {
        $rawOutput = Invoke-Backtest -Strategy $strategy -Timerange $fullSampleRange
        $m = Parse-BacktestOutput $rawOutput

        $avgProfit = "0"
        if ([int]$m.trades -gt 0) {
            $avgProfit = [math]::Round([double]$m.totProfitPct / [int]$m.trades, 4).ToString()
        }

        "$strategy,$group,`"$name`",$($m.trades),$avgProfit,$($m.totProfitUsdt),$($m.totProfitPct),$($m.sharpe),$($m.pf),$($m.maxDD),$($m.winRate),$($m.cagr),$($m.sortino),`"$paramsJson`"" | Out-File $resultsCsv -Append -Encoding utf8

        $color = if ([double]$m.sharpe -gt 0.5) { "Green" } elseif ([double]$m.sharpe -gt 0) { "Yellow" } else { "Red" }
        Write-Host "  -> Trades=$($m.trades)  Sharpe=$($m.sharpe)  PF=$($m.pf)  Profit=$($m.totProfitPct)%  DD=$($m.maxDD)%" -ForegroundColor $color
        $s1Completed++

        if ([double]$m.sharpe -ge 0.6) {
            ($rawOutput -join "`n") | Out-File "$resultsDir/V6_${strategy}_raw.txt" -Encoding utf8
        }
    }
    catch {
        Write-Host "  -> FAILED: $_" -ForegroundColor Red
        "$strategy,$group,`"$name`",FAILED,,,,,,,,,,`"$paramsJson`"" | Out-File $resultsCsv -Append -Encoding utf8
        $s1Failed++
    }
}

Write-Host ""
Write-Host "STAGE 1 DONE: total=$total completed=$s1Completed failed=$s1Failed skipped=$($completedStrategies.Count)" -ForegroundColor $(if ($s1Failed -eq 0) { "Green" } else { "Yellow" })

# ========== Stage 1.5 — Gate filter ==========
$s1MinSharpe = [double]$gates.stage1.min_sharpe
$s1MinPF     = [double]$gates.stage1.min_pf
$s1MinTrades = [int]$gates.stage1.min_trades
$s1MaxDD     = [double]$gates.stage1.max_dd

Write-PhaseBanner "STAGE 1.5 — Gate filter (Sharpe>$s1MinSharpe PF>$s1MinPF trades>$s1MinTrades DD<$s1MaxDD%)"

$phase1Candidates = @()
$rows = Import-Csv $resultsCsv
foreach ($r in $rows) {
    if ($r.trades -eq "FAILED") { continue }
    try {
        $t = [int]$r.trades
        $sh = [double]$r.sharpe
        $pfv = [double]$r.profit_factor
        $dd = [double]$r.max_drawdown_pct
        if ($sh -gt $s1MinSharpe -and $pfv -gt $s1MinPF -and $t -gt $s1MinTrades -and $dd -lt $s1MaxDD) {
            $phase1Candidates += $r
        }
    }
    catch { }
}

Write-Host "Candidates passing S1 gate: $($phase1Candidates.Count)" -ForegroundColor Green
foreach ($c in $phase1Candidates) {
    Write-Host ("  * {0,-40}  Sharpe={1}  PF={2}  Trades={3}" -f $c.strategy, $c.sharpe, $c.profit_factor, $c.trades) -ForegroundColor Cyan
}

# ========== Stage 2 — Yearly validation ==========
$yearlyPeriods = @()
foreach ($yp in $gates.stage2.yearly_periods) {
    $yearlyPeriods += @{ year = $yp.year; range = $yp.range }
}

$stage2Pass = 0
$stage2Fail = 0
$phase2Survivors = @()

if ($phase1Candidates.Count -eq 0) {
    Write-PhaseBanner "STAGE 2 — SKIPPED (no S1 candidates)"
}
else {
    Write-PhaseBanner "STAGE 2 — Yearly validation ($($phase1Candidates.Count) candidates x $($yearlyPeriods.Count) years)"

    $stage2Start = Get-Date
    $yearlyDone = @{}
    if (Test-Path $yearlyCsv) {
        $yl = Import-Csv $yearlyCsv -ErrorAction SilentlyContinue
        foreach ($row in $yl) {
            $k = "$($row.strategy)|$($row.year)"
            $yearlyDone[$k] = $true
        }
        Write-Host "Resume: $($yearlyDone.Count) yearly rows already done" -ForegroundColor Yellow
    }
    else {
        "strategy,group,name,year,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino" | Out-File $yearlyCsv -Encoding utf8
    }

    $totalS2 = $phase1Candidates.Count * $yearlyPeriods.Count
    $idxS2 = 0

    foreach ($c in $phase1Candidates) {
        $strategy = $c.strategy
        $group = $c.group
        $name = $c.name

        foreach ($p in $yearlyPeriods) {
            $key = "$strategy|$($p.year)"
            if ($yearlyDone.ContainsKey($key)) {
                $idxS2++
                continue
            }

            $idxS2++
            $pct = [math]::Round(($idxS2 / $totalS2) * 100, 0)
            $etaMin = if ($idxS2 -gt 1) {
                $el = (Get-Date) - $stage2Start
                [math]::Round(($el.TotalMinutes / ($idxS2 - 1)) * ($totalS2 - $idxS2 + 1), 0)
            }
            else { "?" }
            Write-Host "[$idxS2/$totalS2] ($pct%) $strategy / $($p.year)  ETA:~${etaMin}m" -ForegroundColor Cyan

            try {
                $raw = Invoke-Backtest -Strategy $strategy -Timerange $p.range -StrategyPath $StrategyPathDocker
                $m = Parse-BacktestOutput $raw
                "$strategy,$group,`"$name`",$($p.year),$($p.range),$($m.trades),$($m.totProfitPct),$($m.sharpe),$($m.pf),$($m.maxDD),$($m.winRate),$($m.cagr),$($m.sortino)" | Out-File $yearlyCsv -Append -Encoding utf8
                $yearlyDone[$key] = $true

                $clr = if ([double]$m.sharpe -gt 0.3) { "Green" } elseif ([double]$m.sharpe -ge 0) { "Yellow" } else { "Red" }
                Write-Host "  -> Trades=$($m.trades)  Sharpe=$($m.sharpe)  PF=$($m.pf)  Profit=$($m.totProfitPct)%" -ForegroundColor $clr
            }
            catch {
                Write-Host "  -> FAILED: $_" -ForegroundColor Red
                "$strategy,$group,`"$name`",$($p.year),$($p.range),0,0,0,0,0,0,0,0" | Out-File $yearlyCsv -Append -Encoding utf8
                $yearlyDone[$key] = $true
            }
        }
    }

    Write-Host ""
    Write-Host "Evaluating yearly gates..." -ForegroundColor Yellow
    $allYearly = Import-Csv $yearlyCsv
    foreach ($c in $phase1Candidates) {
        $strategy = $c.strategy
        $yearRows = @($allYearly | Where-Object { $_.strategy -eq $strategy })
        $eligible = @($yearRows | Where-Object { [int]$_.trades -ge 50 })
        $profitable = @($eligible | Where-Object { [double]$_.tot_profit_pct -gt 0 })

        $pass = $true
        $reason = "ok"

        if ($eligible.Count -lt 5) {
            $pass = $false; $reason = "eligible years $($eligible.Count) < 5"
        }
        elseif ($profitable.Count -lt 5) {
            $pass = $false; $reason = "profitable years $($profitable.Count) < 5"
        }
        else {
            foreach ($yr in $eligible) {
                if ([double]$yr.sharpe -lt -0.5) {
                    $pass = $false; $reason = "year $($yr.year) Sharpe $($yr.sharpe) < -0.5"
                    break
                }
            }
            $bear = $yearRows | Where-Object { $_.year -eq "2022" } | Select-Object -First 1
            if ($pass -and $bear -and [int]$bear.trades -ge 50 -and [double]$bear.sharpe -le -0.3) {
                $pass = $false; $reason = "2022 bear Sharpe $($bear.sharpe) <= -0.3"
            }
        }

        if ($pass) {
            Write-Host "[PASS yearly] $strategy" -ForegroundColor Green
            $stage2Pass++
            $phase2Survivors += $c
        }
        else {
            Write-Host "[FAIL yearly] $strategy :: $reason" -ForegroundColor Red
            $stage2Fail++
        }
    }

    Write-Host ""
    Write-Host "STAGE 2 DONE: candidates=$($phase1Candidates.Count) pass=$stage2Pass fail=$stage2Fail" -ForegroundColor Cyan
}

# ========== Stage 3 — Walk-Forward ==========
$wfWindows = @()
foreach ($ww in $gates.stage3.walkforward_windows) {
    $wfWindows += @{ id = $ww.name; train = $ww.train; test = $ww.test }
}

$stage3Pass = 0
$stage3Fail = 0

if ($phase2Survivors.Count -eq 0) {
    Write-PhaseBanner "STAGE 3 — SKIPPED (no S2 survivors)"
}
else {
    Write-PhaseBanner "STAGE 3 — Walk-Forward ($($phase2Survivors.Count) survivors x $($wfWindows.Count) windows)"

    $stage3Start = Get-Date
    $wfDone = @{}
    if (Test-Path $wfCsv) {
        $wfExisting = Import-Csv $wfCsv -ErrorAction SilentlyContinue
        foreach ($row in $wfExisting) {
            $k = "$($row.strategy)|$($row.window)|$($row.phase)"
            $wfDone[$k] = $true
        }
    }
    else {
        "strategy,group,name,window,phase,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,cagr,sortino" | Out-File $wfCsv -Encoding utf8
    }

    $totalS3 = $phase2Survivors.Count * $wfWindows.Count * 2
    $idxS3 = 0

    foreach ($c in $phase2Survivors) {
        $strategy = $c.strategy
        $group = $c.group
        $name = $c.name

        foreach ($w in $wfWindows) {
            foreach ($phase in @("train", "test")) {
                $tr = if ($phase -eq "train") { $w.train } else { $w.test }
                $key = "$strategy|$($w.id)|$phase"
                if ($wfDone.ContainsKey($key)) {
                    $idxS3++
                    continue
                }

                $idxS3++
                $pct = if ($totalS3 -gt 0) { [math]::Round(($idxS3 / $totalS3) * 100, 0) } else { 0 }
                Write-Host "[$idxS3/$totalS3] ($pct%) $strategy $($w.id) $phase" -ForegroundColor Cyan

                try {
                    $raw = Invoke-Backtest -Strategy $strategy -Timerange $tr -StrategyPath $StrategyPathDocker
                    $m = Parse-BacktestOutput $raw
                    "$strategy,$group,`"$name`",$($w.id),$phase,$tr,$($m.trades),$($m.totProfitPct),$($m.sharpe),$($m.pf),$($m.maxDD),$($m.cagr),$($m.sortino)" | Out-File $wfCsv -Append -Encoding utf8
                    $wfDone[$key] = $true

                    $clr = if ([double]$m.sharpe -gt 0) { "Green" } else { "Red" }
                    Write-Host "  -> Sharpe=$($m.sharpe) PF=$($m.pf) Profit=$($m.totProfitPct)%" -ForegroundColor $clr
                }
                catch {
                    Write-Host "  -> FAILED: $_" -ForegroundColor Red
                }
            }
        }
    }

    Write-Host ""
    Write-Host "Evaluating walk-forward gates..." -ForegroundColor Yellow
    $allWf = Import-Csv $wfCsv
    foreach ($c in $phase2Survivors) {
        $strategy = $c.strategy
        $pass = $true
        $reason = "ok"

        foreach ($w in $wfWindows) {
            $testRow = $allWf | Where-Object { $_.strategy -eq $strategy -and $_.window -eq $w.id -and $_.phase -eq "test" } | Select-Object -First 1
            $trainRow = $allWf | Where-Object { $_.strategy -eq $strategy -and $_.window -eq $w.id -and $_.phase -eq "train" } | Select-Object -First 1
            if (-not $testRow -or -not $trainRow) { $pass = $false; $reason = "missing $($w.id)"; break }
            if ([double]$testRow.sharpe -le 0) { $pass = $false; $reason = "$($w.id) test Sharpe <= 0"; break }
            $tpf = [double]$testRow.profit_factor
            $trpf = [double]$trainRow.profit_factor
            if ($trpf -gt 0 -and $tpf -lt ($trpf * 0.8)) { $pass = $false; $reason = "$($w.id) PF decay"; break }
        }

        if ($pass) {
            Write-Host "[PASS WF] $strategy" -ForegroundColor Green
            $stage3Pass++
        }
        else {
            Write-Host "[FAIL WF] $strategy :: $reason" -ForegroundColor Red
            $stage3Fail++
        }
    }

    Write-Host "STAGE 3 DONE: in=$($phase2Survivors.Count) pass=$stage3Pass fail=$stage3Fail" -ForegroundColor Cyan
}

# ========== Analysis ==========
Write-PhaseBanner "ANALYSIS — Running analyze_v6.py"

$analyzeScript = "user_data/scripts/analyze_v6.py"
if (Test-Path $analyzeScript) {
    try {
        & python $analyzeScript
        Write-Host "Analysis complete. See experiment_results/v6_analysis.md" -ForegroundColor Green
    }
    catch {
        Write-Host "Analysis failed: $_" -ForegroundColor Yellow
    }
}
else {
    Write-Host "analyze_v6.py not found; skipping." -ForegroundColor Yellow
}

# ========== Summary ==========
$pipelineEnd = Get-Date
$duration = $pipelineEnd - $pipelineStart

$summaryContent = @"
V6 Pipeline Summary
===================
Started:  $($pipelineStart.ToString('MM/dd/yyyy HH:mm:ss'))
Ended:    $($pipelineEnd.ToString('MM/dd/yyyy HH:mm:ss'))
Duration: $("{0:hh\:mm\:ss}" -f $duration)

Stage 1:   completed=$s1Completed failed=$s1Failed resumed=$($completedStrategies.Count)
Stage 1.5: candidates=$($phase1Candidates.Count)
Stage 2:   pass=$stage2Pass fail=$stage2Fail
Stage 3:   pass=$stage3Pass fail=$stage3Fail

"@

$summaryContent | Out-File $summaryFile -Encoding utf8
Write-Host $summaryContent -ForegroundColor Magenta
Write-Host "Pipeline complete!" -ForegroundColor Green
