#Requires -Version 5.1
<#
.SYNOPSIS
    V4 三阶段流水线回测：全样本筛选 → 分年度验证 → Walk-Forward → 分析脚本
.DESCRIPTION
    工作目录固定为 c:\Users\hlin2\freqtrade；Docker 执行 freqtrade backtesting。
#>

$ErrorActionPreference = "Continue"
$pipelineStart = Get-Date
$workDir = "c:\Users\hlin2\freqtrade"
Set-Location $workDir

$manifestPath = "user_data/experiment_manifest_v4.json"
$resultsDir = "user_data/experiment_results"
$resultsCsv = "$resultsDir/v4_results.csv"
$yearlyCsv = "$resultsDir/v4_yearly.csv"
$wfCsv = "$resultsDir/v4_walkforward.csv"
$progressFile = "$resultsDir/v4_progress.txt"

$DockerImage = "freqtradeorg/freqtrade:stable"
$StrategyPathDocker = "/freqtrade/user_data/strategies/experiments_v4"
$DefaultConfigDocker = "/freqtrade/user_data/config_backtest.json"

# --- helpers: console ---
function Write-PhaseBanner([string]$Title) {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Magenta
    Write-Host " $Title" -ForegroundColor Magenta
    Write-Host ("=" * 60) -ForegroundColor Magenta
    Write-Host ""
}

function Resolve-ConfigDockerPath($exp) {
    if ($null -ne $exp.config -and "$($exp.config)".Trim().Length -gt 0) {
        $c = "$($exp.config)".Trim() -replace '\\', '/'
        if ($c.StartsWith('/freqtrade/')) { return $c }
        if ($c.StartsWith('user_data/')) { return "/freqtrade/$c" }
        return "/freqtrade/user_data/$c"
    }
    return $DefaultConfigDocker
}

function Parse-BacktestOutput([object[]]$rawOutput) {
    $trades = "0"; $totProfitPct = "0"; $totProfitUsdt = "0"
    $sharpe = "0"; $pf = "0"; $maxDD = "0"; $cagr = "0"; $sortino = "0"; $winRate = "0"
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
    }
}

function Invoke-V4Backtest {
    param(
        [string]$Strategy,
        [string]$Timerange,
        [string]$ConfigDocker,
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

function Test-YearlySurvivor {
    param([System.Collections.Generic.List[object]]$Rows)
    $minTradesPerYear = [int]$gates.stage2.min_trades_per_year
    $minEligibleYears = [int]$gates.stage2.min_eligible_years
    $minProfitableYears = [int]$gates.stage2.min_profitable_years
    $maxSharpeFloor = [double]$gates.stage2.max_sharpe_floor
    $bearYear = $gates.stage2.bear_year
    $bearMinSharpe = [double]$gates.stage2.bear_min_sharpe

    $eligible = @($Rows | Where-Object { [int]$_.trades -ge $minTradesPerYear })
    if ($eligible.Count -lt $minEligibleYears) {
        return @{ ok = $false; reason = "eligible_years_lt$minEligibleYears ($($eligible.Count) need trades>=$minTradesPerYear)" }
    }
    $pos = @($eligible | Where-Object { [double]$_.tot_profit_pct -gt 0 }).Count
    $needPos = [math]::Ceiling($minProfitableYears / 6.0 * $eligible.Count)
    if ($needPos -lt $minProfitableYears) { $needPos = $minProfitableYears }
    if ($pos -lt $needPos) {
        return @{ ok = $false; reason = "profitable_years $pos < $needPos (among eligible=$($eligible.Count))" }
    }
    foreach ($r in $eligible) {
        $s = [double]$r.sharpe
        if ($s -lt $maxSharpeFloor) {
            return @{ ok = $false; reason = "year $($r.year) Sharpe $s < $maxSharpeFloor" }
        }
    }
    $yBear = $Rows | Where-Object { $_.year -eq $bearYear } | Select-Object -First 1
    if ($yBear -and [int]$yBear.trades -ge $minTradesPerYear) {
        if ([double]$yBear.sharpe -le $bearMinSharpe) {
            return @{ ok = $false; reason = "$bearYear Sharpe $($yBear.sharpe) not > $bearMinSharpe" }
        }
    }
    return @{ ok = $true; reason = "ok" }
}

function Test-WalkForwardSurvivor {
    param([System.Collections.Generic.List[object]]$Rows)
    $pfDecayThreshold = [double]$gates.stage3.pf_decay_threshold
    $wfNames = @()
    foreach ($ww in $gates.stage3.walkforward_windows) { $wfNames += $ww.name }
    foreach ($w in $wfNames) {
        $testRow = $Rows | Where-Object { $_.window -eq $w -and $_.phase -eq "test" } | Select-Object -First 1
        $trainRow = $Rows | Where-Object { $_.window -eq $w -and $_.phase -eq "train" } | Select-Object -First 1
        if (-not $testRow -or -not $trainRow) {
            return @{ ok = $false; reason = "missing rows for $w" }
        }
        if ([double]$testRow.sharpe -le 0) {
            return @{ ok = $false; reason = "$w test Sharpe $($testRow.sharpe) not > 0" }
        }
        $tpf = [double]$testRow.profit_factor
        $trpf = [double]$trainRow.profit_factor
        $floor = $trpf * $pfDecayThreshold
        if ($tpf -lt $floor) {
            return @{ ok = $false; reason = "$w test PF $tpf < train PF $trpf * $pfDecayThreshold ($floor)" }
        }
    }
    return @{ ok = $true; reason = "ok" }
}

if (-not (Test-Path $resultsDir)) { New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null }

# --- Load unified gate config ---
$gatesJsonPath = "user_data/configs/experiment_gates.json"
if (-not (Test-Path $gatesJsonPath)) {
    Write-Host "FATAL: Gates config not found: $gatesJsonPath" -ForegroundColor Red
    exit 1
}
$gates = Get-Content $gatesJsonPath -Raw | ConvertFrom-Json

if (-not (Test-Path $manifestPath)) {
    Write-Host "FATAL: Manifest not found: $manifestPath" -ForegroundColor Red
    exit 1
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$manifestByStrategy = @{}
foreach ($e in $manifest) { $manifestByStrategy[$e.strategy] = $e }

$fullSampleRange = $gates.full_sample_timerange

# ========== Stage 1 ==========
Write-PhaseBanner "STAGE 1 — Full-sample screen ($fullSampleRange)"

$stage1Start = Get-Date
$s1Completed = 0
$s1Failed = 0
$s1Skipped = 0

$completedStrategies = @{}
if (Test-Path $resultsCsv) {
    $existingLines = Get-Content $resultsCsv -ErrorAction SilentlyContinue | Select-Object -Skip 1
    foreach ($line in $existingLines) {
        if ($line -match "^([^,]+),") { $completedStrategies[$Matches[1]] = $true }
    }
    Write-Host "Resume: $($completedStrategies.Count) strategies already in v4_results.csv (skip)." -ForegroundColor Yellow
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
Write-Host "Manifest experiments: $total | Remaining to run: $totalRemaining" -ForegroundColor Cyan
Write-Host ""

for ($i = 0; $i -lt $totalRemaining; $i++) {
    $exp = $remaining[$i]
    $strategy = $exp.strategy
    $group = $exp.group
    $name = $exp.name
    $paramsObj = $exp.params
    if ($null -eq $paramsObj) { $paramsObj = @{} }
    $paramsJson = ($paramsObj | ConvertTo-Json -Compress -Depth 10) -replace '"', '""'
    $cfg = Resolve-ConfigDockerPath $exp

    $elapsed = (Get-Date) - $stage1Start
    $globalIdx = $completedStrategies.Count + $i + 1
    $pct = if ($total -gt 0) { [math]::Round(($globalIdx / $total) * 100, 1) } else { 0 }
    $etaMin = if ($i -gt 0) { [math]::Round(($elapsed.TotalMinutes / $i) * ($totalRemaining - $i), 0) } else { "?" }

    Write-Host "[$globalIdx/$total] ($pct%) $group :: $name  ETA:~${etaMin}min  cfg=$cfg" -ForegroundColor Cyan
    "$(Get-Date -Format 'HH:mm:ss') [$globalIdx/$total] $strategy - $name" | Out-File $progressFile -Append -Encoding utf8

    try {
        $rawOutput = Invoke-V4Backtest -Strategy $strategy -Timerange $fullSampleRange -ConfigDocker $cfg
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
            ($rawOutput -join "`n") | Out-File "$resultsDir/V4_${strategy}_raw.txt" -Encoding utf8
        }
    }
    catch {
        Write-Host "  -> FAILED: $_" -ForegroundColor Red
        "$strategy,$group,`"$name`",FAILED,,,,,,,,,,`"$paramsJson`"" | Out-File $resultsCsv -Append -Encoding utf8
        $s1Failed++
    }
}

$s1Skipped = $completedStrategies.Count
Write-Host ""
Write-Host "STAGE 1 SUMMARY:  manifest=$total  newly_completed=$s1Completed  failed=$s1Failed  skipped(resume)=$s1Skipped" -ForegroundColor $(if ($s1Failed -eq 0) { "Green" } else { "Yellow" })

# ========== Stage 1.5 ==========
$s1MinSharpe = [double]$gates.stage1.min_sharpe
$s1MinPF     = [double]$gates.stage1.min_pf
$s1MinTrades = [int]$gates.stage1.min_trades
$s1MaxDD     = [double]$gates.stage1.max_dd

Write-PhaseBanner "STAGE 1.5 — Auto gate (Sharpe>$s1MinSharpe, PF>$s1MinPF, trades>$s1MinTrades, DD<$s1MaxDD%)"

$phase1Candidates = @()
if (-not (Test-Path $resultsCsv)) {
    Write-Host "No results CSV; no candidates." -ForegroundColor Red
}
else {
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
}

Write-Host "Candidates passing gate: $($phase1Candidates.Count)" -ForegroundColor Green
foreach ($c in $phase1Candidates) {
    Write-Host ("  * {0,-40}  Sharpe={1}  PF={2}  Trades={3}" -f $c.strategy, $c.sharpe, $c.profit_factor, $c.trades) -ForegroundColor Cyan
}

# ========== Stage 2 ==========
$yearlyPeriods = @()
foreach ($yp in $gates.stage2.yearly_periods) {
    $yearlyPeriods += @{ year = $yp.year; range = $yp.range }
}

$stage2Pass = 0
$stage2Fail = 0
$phase2Survivors = @()

if ($phase1Candidates.Count -eq 0) {
    Write-PhaseBanner "STAGE 2 — SKIPPED (no phase-1 candidates)"
}
else {
    Write-PhaseBanner "STAGE 2 — Yearly validation (candidates x 6)"

    $stage2Start = Get-Date
    $yearlyDone = @{}
    if (Test-Path $yearlyCsv) {
        $yl = Import-Csv $yearlyCsv -ErrorAction SilentlyContinue
        foreach ($row in $yl) {
            $k = "$($row.strategy)|$($row.year)|$($row.timerange)"
            $yearlyDone[$k] = $true
        }
        Write-Host "Resume: $($yearlyDone.Count) yearly rows already in v4_yearly.csv" -ForegroundColor Yellow
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
        $exp = $manifestByStrategy[$strategy]
        $cfg = if ($exp) { Resolve-ConfigDockerPath $exp } else { $DefaultConfigDocker }

        foreach ($p in $yearlyPeriods) {
            $key = "$strategy|$($p.year)|$($p.range)"
            if ($yearlyDone.ContainsKey($key)) {
                Write-Host "[skip] $strategy / $($p.year) (already in CSV)" -ForegroundColor DarkGray
                continue
            }

            $idxS2++
            $pct = [math]::Round(($idxS2 / $totalS2) * 100, 0)
            $etaMin = if ($idxS2 -gt 1) {
                $el = (Get-Date) - $stage2Start
                [math]::Round(($el.TotalMinutes / ($idxS2 - 1)) * ($totalS2 - $idxS2 + 1), 0)
            }
            else { "?" }
            Write-Host "[$idxS2/~$totalS2] (~$pct%) $strategy / $($p.year)  ETA:~${etaMin}m" -ForegroundColor Cyan

            try {
                $raw = Invoke-V4Backtest -Strategy $strategy -Timerange $p.range -ConfigDocker $cfg
                $m = Parse-BacktestOutput $raw
                "$strategy,$group,`"$name`",$($p.year),$($p.range),$($m.trades),$($m.totProfitPct),$($m.sharpe),$($m.pf),$($m.maxDD),$($m.winRate),$($m.cagr),$($m.sortino)" | Out-File $yearlyCsv -Append -Encoding utf8
                $yearlyDone[$key] = $true

                $clr = if ([double]$m.sharpe -gt 0.3) { "Green" } elseif ([double]$m.sharpe -ge 0) { "Yellow" } else { "Red" }
                Write-Host "  -> Trades=$($m.trades)  Sharpe=$($m.sharpe)  PF=$($m.pf)  Profit=$($m.totProfitPct)%" -ForegroundColor $clr

                if ([double]$m.sharpe -ge 0.6) {
                    ($raw -join "`n") | Out-File "$resultsDir/V4_${strategy}_$($p.year)_raw.txt" -Encoding utf8
                }
            }
            catch {
                Write-Host "  -> FAILED: $_" -ForegroundColor Red
            }
        }
    }

    Write-Host ""
    Write-Host "Evaluating yearly gates..." -ForegroundColor Yellow
    $allYearly = Import-Csv $yearlyCsv
    foreach ($c in $phase1Candidates) {
        $strategy = $c.strategy
        $strRows = [System.Collections.Generic.List[object]]::new()
        foreach ($yr in $yearlyPeriods) {
            $hit = $allYearly | Where-Object { $_.strategy -eq $strategy -and $_.year -eq $yr.year } | Select-Object -First 1
            if ($hit) { $strRows.Add($hit) }
        }
        $ev = Test-YearlySurvivor -Rows $strRows
        if ($ev.ok) {
            Write-Host "[PASS yearly] $strategy" -ForegroundColor Green
            $stage2Pass++
            $phase2Survivors += $c
        }
        else {
            Write-Host "[FAIL yearly] $strategy :: $($ev.reason)" -ForegroundColor Red
            $stage2Fail++
        }
    }

    Write-Host ""
    Write-Host "STAGE 2 SUMMARY:  candidates=$($phase1Candidates.Count)  pass=$stage2Pass  fail=$stage2Fail" -ForegroundColor $(if ($stage2Fail -eq 0) { "Green" } else { "Cyan" })
}

# ========== Stage 3 ==========
$wfWindows = @()
foreach ($ww in $gates.stage3.walkforward_windows) {
    $wfWindows += @{ id = $ww.name; train = $ww.train; test = $ww.test }
}

$stage3Pass = 0
$stage3Fail = 0

if ($phase2Survivors.Count -eq 0) {
    Write-PhaseBanner "STAGE 3 — SKIPPED (no phase-2 survivors)"
}
else {
    Write-PhaseBanner "STAGE 3 — Walk-forward (train+test per window x3)"

    $stage3Start = Get-Date
    $wfDone = @{}
    if (Test-Path $wfCsv) {
        $wfExisting = Import-Csv $wfCsv -ErrorAction SilentlyContinue
        foreach ($row in $wfExisting) {
            $k = "$($row.strategy)|$($row.window)|$($row.phase)|$($row.timerange)"
            $wfDone[$k] = $true
        }
        Write-Host "Resume: $($wfDone.Count) walk-forward rows in v4_walkforward.csv" -ForegroundColor Yellow
    }
    else {
        "strategy,group,name,window,phase,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,cagr,sortino" | Out-File $wfCsv -Encoding utf8
    }

    $runsPerStrategy = $wfWindows.Count * 2
    $totalS3 = $phase2Survivors.Count * $runsPerStrategy
    $idxS3 = 0

    foreach ($c in $phase2Survivors) {
        $strategy = $c.strategy
        $group = $c.group
        $name = $c.name
        $exp = $manifestByStrategy[$strategy]
        $cfg = if ($exp) { Resolve-ConfigDockerPath $exp } else { $DefaultConfigDocker }

        foreach ($w in $wfWindows) {
            foreach ($phase in @("train", "test")) {
                $tr = if ($phase -eq "train") { $w.train } else { $w.test }
                $key = "$strategy|$($w.id)|$phase|$tr"
                if ($wfDone.ContainsKey($key)) {
                    Write-Host "[skip] $strategy $($w.id) $phase $tr" -ForegroundColor DarkGray
                    continue
                }

                $idxS3++
                $pct = if ($totalS3 -gt 0) { [math]::Round(($idxS3 / $totalS3) * 100, 0) } else { 0 }
                $etaMin = if ($idxS3 -gt 1) {
                    $el = (Get-Date) - $stage3Start
                    [math]::Round(($el.TotalMinutes / ($idxS3 - 1)) * ($totalS3 - $idxS3 + 1), 0)
                }
                else { "?" }
                Write-Host "[$idxS3/$totalS3] ($pct%) $strategy $($w.id) $phase $tr ETA:~${etaMin}m" -ForegroundColor Cyan

                try {
                    $raw = Invoke-V4Backtest -Strategy $strategy -Timerange $tr -ConfigDocker $cfg
                    $m = Parse-BacktestOutput $raw
                    "$strategy,$group,`"$name`",$($w.id),$phase,$tr,$($m.trades),$($m.totProfitPct),$($m.sharpe),$($m.pf),$($m.maxDD),$($m.cagr),$($m.sortino)" | Out-File $wfCsv -Append -Encoding utf8
                    $wfDone[$key] = $true

                    $clr = if ([double]$m.sharpe -gt 0) { "Green" } elseif ([double]$m.sharpe -ge -0.2) { "Yellow" } else { "Red" }
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
        $strRows = [System.Collections.Generic.List[object]]::new()
        foreach ($row in $allWf) {
            if ($row.strategy -eq $strategy) { $strRows.Add($row) }
        }
        $ev = Test-WalkForwardSurvivor -Rows $strRows
        if ($ev.ok) {
            Write-Host "[PASS WF] $strategy" -ForegroundColor Green
            $stage3Pass++
        }
        else {
            Write-Host "[FAIL WF] $strategy :: $($ev.reason)" -ForegroundColor Red
            $stage3Fail++
        }
    }

    Write-Host ""
    Write-Host "STAGE 3 SUMMARY:  survivors_in=$($phase2Survivors.Count)  pass=$stage3Pass  fail=$stage3Fail" -ForegroundColor Cyan
}

# ========== Stage 4 ==========
Write-PhaseBanner "STAGE 4 — analyze_v4.py"

$analyzeScript = "user_data/scripts/analyze_v4.py"
$analyzeRan = $false
if (Test-Path $analyzeScript) {
    $pyCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pyCmd) {
        Write-Host "Running local: python $analyzeScript" -ForegroundColor Cyan
        try {
            & python $analyzeScript
            if ($LASTEXITCODE -eq 0) { $analyzeRan = $true }
        }
        catch {
            Write-Host "Local python failed: $_" -ForegroundColor Yellow
        }
    }
    if (-not $analyzeRan) {
        Write-Host "Running Docker: python /freqtrade/user_data/scripts/analyze_v4.py" -ForegroundColor Cyan
        docker run --rm `
            -v "./user_data:/freqtrade/user_data" `
            $DockerImage python /freqtrade/user_data/scripts/analyze_v4.py 2>&1
    }
}
else {
    Write-Host "Skip: $analyzeScript not found." -ForegroundColor Yellow
}

# ========== Final ==========
$pipelineEnd = Get-Date
$dur = $pipelineEnd - $pipelineStart

Write-Host ""
Write-PhaseBanner "PIPELINE COMPLETE"
Write-Host ("Total wall time: {0}" -f $dur.ToString('hh\:mm\:ss')) -ForegroundColor Green
Write-Host ""
Write-Host "Stage 1: full-sample -> $resultsCsv"
Write-Host "Stage 1.5: gate -> $($phase1Candidates.Count) candidates"
Write-Host "Stage 2: yearly -> $yearlyCsv  (pass $stage2Pass / fail $stage2Fail)"
Write-Host "Stage 3: walk-forward -> $wfCsv  (pass $stage3Pass / fail $stage3Fail)"
Write-Host ""

@"
V4 Pipeline Summary
===================
Started:  $pipelineStart
Ended:    $pipelineEnd
Duration: $($dur.ToString('hh\:mm\:ss'))

Stage 1:   completed_new=$s1Completed failed=$s1Failed resume_skipped=$s1Skipped
Stage 1.5: candidates=$($phase1Candidates.Count)
Stage 2:   pass=$stage2Pass fail=$stage2Fail (if run)
Stage 3:   pass=$stage3Pass fail=$stage3Fail (if run)
"@ | Out-File "$resultsDir/v4_pipeline_summary.txt" -Encoding utf8

Write-Host "Summary written: $resultsDir/v4_pipeline_summary.txt" -ForegroundColor Cyan
