#Requires -Version 5.1
<#
.SYNOPSIS
    V5 实验流水线：新币数据下载 → 策略优化三阶段（全样本→年度→WF）→ 分析 → 新币 CryptoV11 筛选
.DESCRIPTION
    Pipeline-1 与 V4 结构一致（manifest v5 / experiments_v5）；Pipeline-2 对 12 个新币做单币回测与年度验证。
#>

$ErrorActionPreference = "Continue"
$pipelineStart = Get-Date

$workDir = "c:\Users\hlin2\freqtrade"
$DockerImage = "freqtradeorg/freqtrade:stable"
$StrategyPathDocker = "/freqtrade/user_data/strategies/experiments_v5"
$DefaultConfigDocker = "/freqtrade/user_data/config_backtest.json"
$CryptoV11StrategyPath = "/freqtrade/user_data/strategies"

Set-Location $workDir

$manifestPath = "user_data/experiment_manifest_v5.json"
$resultsDir = "user_data/experiment_results"
$resultsCsv = "$resultsDir/v5_results.csv"
$yearlyCsv = "$resultsDir/v5_yearly.csv"
$wfCsv = "$resultsDir/v5_walkforward.csv"
$progressFile = "$resultsDir/v5_progress.txt"
$pairScreenCsv = "$resultsDir/v5_pair_screening.csv"
$summaryFile = "$resultsDir/v5_pipeline_summary.txt"
$configsV5Dir = "user_data/configs_v5"
$baseConfigPath = "user_data/config_backtest.json"

$newPairs = @(
    "DOT/USDT:USDT", "LTC/USDT:USDT", "ATOM/USDT:USDT", "NEAR/USDT:USDT",
    "APT/USDT:USDT", "ARB/USDT:USDT", "OP/USDT:USDT", "INJ/USDT:USDT",
    "SUI/USDT:USDT", "TRX/USDT:USDT", "UNI/USDT:USDT", "FIL/USDT:USDT"
)

# --- helpers: console ---
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

function Invoke-Backtest {
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

function New-PairScreenConfigFile {
    param(
        [string]$Pair,
        [int]$Index
    )
    if (-not (Test-Path $baseConfigPath)) {
        throw "Base config missing: $baseConfigPath"
    }
    $idxStr = "{0:D3}" -f $Index
    $safe = ($Pair -replace '[/:]', '_')
    $fileName = "pair_screen_${idxStr}_$safe.json"
    $relPath = "$configsV5Dir/$fileName"
    $full = Join-Path $workDir $relPath
    if (-not (Test-Path $configsV5Dir)) {
        New-Item -ItemType Directory -Path $configsV5Dir -Force | Out-Null
    }
    $j = Get-Content $baseConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $j.exchange.pair_whitelist = @($Pair)
    if ($null -eq $j.max_open_trades) { $j | Add-Member -NotePropertyName max_open_trades -NotePropertyValue 1 -Force }
    else { $j.max_open_trades = 1 }
    $j | ConvertTo-Json -Depth 20 | Out-File -FilePath $full -Encoding utf8
    return "/freqtrade/$($relPath -replace '\\', '/')"
}

if (-not (Test-Path $resultsDir)) { New-Item -ItemType Directory -Path $resultsDir -Force | Out-Null }

# --- Load unified gate config ---
$gatesJsonPath = "user_data/configs/experiment_gates.json"
if (-not (Test-Path $gatesJsonPath)) {
    Write-Host "FATAL: Gates config not found: $gatesJsonPath" -ForegroundColor Red
    exit 1
}
$gates = Get-Content $gatesJsonPath -Raw | ConvertFrom-Json

$fullSampleRange = $gates.full_sample_timerange

# ========== Phase 0 — Download data for new pairs ==========
Write-PhaseBanner "PHASE 0 — Download 15m + 4h data for 12 new pairs (20200101-20260405)"

$dlStart = Get-Date
$dlOk = 0
$dlFail = 0
$dlIdx = 0
foreach ($pair in $newPairs) {
    $dlIdx++
    $elapsed = (Get-Date) - $dlStart
    $etaMin = if ($dlIdx -gt 1) { [math]::Round(($elapsed.TotalMinutes / ($dlIdx - 1)) * ($newPairs.Count - $dlIdx + 1), 0) } else { "?" }
    Write-Log "Download [$dlIdx/$($newPairs.Count)] $pair  ETA:~${etaMin}m"
    "$(Get-Date -Format 'HH:mm:ss') [DL $dlIdx/$($newPairs.Count)] $pair" | Out-File $progressFile -Append -Encoding utf8
    try {
        $dlOut = docker run --rm `
            -v "./user_data:/freqtrade/user_data" `
            $DockerImage download-data `
            --config $DefaultConfigDocker `
            --pairs $pair `
            --timeframes 15m 4h `
            --timerange 20200101-20260405 `
            --trading-mode futures `
            --exchange binance 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  -> download exit code $LASTEXITCODE for $pair" -ForegroundColor Yellow
            ($dlOut | ForEach-Object { $_.ToString() }) | Out-File "$resultsDir/v5_dl_fail_${dlIdx}.log" -Encoding utf8
            $dlFail++
        }
        else {
            $dlOk++
        }
    }
    catch {
        Write-Host "  -> DOWNLOAD FAILED $pair : $_" -ForegroundColor Red
        $dlFail++
    }
}
Write-Host "PHASE 0 SUMMARY: ok=$dlOk failed=$dlFail (failures logged; pipeline continues)" -ForegroundColor $(if ($dlFail -eq 0) { "Green" } else { "Yellow" })

# ========== PIPELINE-1: Strategy optimization ==========
if (-not (Test-Path $manifestPath)) {
    Write-Host "FATAL: Manifest not found: $manifestPath" -ForegroundColor Red
    exit 1
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json
$manifestByStrategy = @{}
foreach ($e in $manifest) { $manifestByStrategy[$e.strategy] = $e }

# ========== Stage 1 ==========
Write-PhaseBanner "PIPELINE-1 / STAGE 1 — Full-sample screen ($fullSampleRange)"

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
    Write-Host "Resume: $($completedStrategies.Count) strategies already in v5_results.csv (skip)." -ForegroundColor Yellow
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
    "$(Get-Date -Format 'HH:mm:ss') [S1 $globalIdx/$total] $strategy - $name" | Out-File $progressFile -Append -Encoding utf8

    try {
        $rawOutput = Invoke-Backtest -Strategy $strategy -Timerange $fullSampleRange -ConfigDocker $cfg
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
            ($rawOutput -join "`n") | Out-File "$resultsDir/V5_${strategy}_raw.txt" -Encoding utf8
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

Write-PhaseBanner "PIPELINE-1 / STAGE 1.5 — Auto gate (Sharpe>$s1MinSharpe, PF>$s1MinPF, trades>$s1MinTrades, DD<$s1MaxDD%)"

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
    Write-PhaseBanner "PIPELINE-1 / STAGE 2 — SKIPPED (no phase-1 candidates)"
}
else {
    Write-PhaseBanner "PIPELINE-1 / STAGE 2 — Yearly validation (candidates x $($yearlyPeriods.Count))"

    $stage2Start = Get-Date
    $yearlyDone = @{}
    if (Test-Path $yearlyCsv) {
        $yl = Import-Csv $yearlyCsv -ErrorAction SilentlyContinue
        foreach ($row in $yl) {
            $k = "$($row.strategy)|$($row.year)|$($row.timerange)"
            $yearlyDone[$k] = $true
        }
        Write-Host "Resume: $($yearlyDone.Count) yearly rows already in v5_yearly.csv" -ForegroundColor Yellow
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
                $raw = Invoke-Backtest -Strategy $strategy -Timerange $p.range -ConfigDocker $cfg
                $m = Parse-BacktestOutput $raw
                "$strategy,$group,`"$name`",$($p.year),$($p.range),$($m.trades),$($m.totProfitPct),$($m.sharpe),$($m.pf),$($m.maxDD),$($m.winRate),$($m.cagr),$($m.sortino)" | Out-File $yearlyCsv -Append -Encoding utf8
                $yearlyDone[$key] = $true

                $clr = if ([double]$m.sharpe -gt 0.3) { "Green" } elseif ([double]$m.sharpe -ge 0) { "Yellow" } else { "Red" }
                Write-Host "  -> Trades=$($m.trades)  Sharpe=$($m.sharpe)  PF=$($m.pf)  Profit=$($m.totProfitPct)%" -ForegroundColor $clr

                if ([double]$m.sharpe -ge 0.6) {
                    ($raw -join "`n") | Out-File "$resultsDir/V5_${strategy}_$($p.year)_raw.txt" -Encoding utf8
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
    Write-PhaseBanner "PIPELINE-1 / STAGE 3 — SKIPPED (no phase-2 survivors)"
}
else {
    Write-PhaseBanner "PIPELINE-1 / STAGE 3 — Walk-forward (train+test per window x$($wfWindows.Count))"

    $stage3Start = Get-Date
    $wfDone = @{}
    if (Test-Path $wfCsv) {
        $wfExisting = Import-Csv $wfCsv -ErrorAction SilentlyContinue
        foreach ($row in $wfExisting) {
            $k = "$($row.strategy)|$($row.window)|$($row.phase)|$($row.timerange)"
            $wfDone[$k] = $true
        }
        Write-Host "Resume: $($wfDone.Count) walk-forward rows in v5_walkforward.csv" -ForegroundColor Yellow
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
                    $raw = Invoke-Backtest -Strategy $strategy -Timerange $tr -ConfigDocker $cfg
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
Write-PhaseBanner "PIPELINE-1 / STAGE 4 — analyze_v5.py"

$analyzeScript = "user_data/scripts/analyze_v5.py"
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
        Write-Host "Running Docker: python /freqtrade/user_data/scripts/analyze_v5.py" -ForegroundColor Cyan
        try {
            docker run --rm `
                -v "./user_data:/freqtrade/user_data" `
                $DockerImage python /freqtrade/user_data/scripts/analyze_v5.py 2>&1
        }
        catch {
            Write-Host "Docker analyze failed: $_" -ForegroundColor Yellow
        }
    }
}
else {
    Write-Host "Skip: $analyzeScript not found." -ForegroundColor Yellow
}

# ========== PIPELINE-2 — New pair screening (CryptoV11) ==========
Write-PhaseBanner "PIPELINE-2 — CryptoV11 new-pair screening ($fullSampleRange)"

$pairRankings = [System.Collections.Generic.List[object]]::new()
$pairScreenResume = @{}
$pairScreenRowByPair = @{}

if (Test-Path $pairScreenCsv) {
    $existingPs = Import-Csv $pairScreenCsv -ErrorAction SilentlyContinue
    foreach ($er in $existingPs) {
        if ($er.pair) {
            $pairScreenResume[$er.pair] = $true
            $pairScreenRowByPair[$er.pair] = $er
        }
    }
    Write-Host "Resume: $($pairScreenResume.Count) pairs already in v5_pair_screening.csv" -ForegroundColor Yellow
}
else {
    "pair,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino,yearly_pass,yearly_detail" | Out-File $pairScreenCsv -Encoding utf8
}

$psStart = Get-Date
$psIdx = 0
$pairYearlyPassCount = 0
$pairYearlyFailCount = 0
$pairYearlySkippedCount = 0

foreach ($pair in $newPairs) {
    $psIdx++
    if ($pairScreenResume.ContainsKey($pair)) {
        Write-Host "[skip] pair screening resume: $pair" -ForegroundColor DarkGray
        if ($pairScreenRowByPair.ContainsKey($pair)) { $pairRankings.Add($pairScreenRowByPair[$pair]) }
        continue
    }

    $elapsed = (Get-Date) - $psStart
    $doneSoFar = $psIdx - 1
    $etaMin = if ($doneSoFar -gt 0) { [math]::Round(($elapsed.TotalMinutes / $doneSoFar) * ($newPairs.Count - $psIdx + 1), 0) } else { "?" }
    Write-Log "Pair screen [$psIdx/$($newPairs.Count)] $pair  ETA:~${etaMin}m"
    "$(Get-Date -Format 'HH:mm:ss') [PS $psIdx/$($newPairs.Count)] $pair" | Out-File $progressFile -Append -Encoding utf8

    $cfgDocker = $null
    try {
        $cfgDocker = New-PairScreenConfigFile -Pair $pair -Index $psIdx
    }
    catch {
        Write-Host "  -> config build FAILED: $_" -ForegroundColor Red
        "`"$pair`",,,,,,,,,SKIPPED,`"config_error`"" | Out-File $pairScreenCsv -Append -Encoding utf8
        $pairRankings.Add([PSCustomObject]@{
                pair = $pair; trades = ""; tot_profit_pct = ""; sharpe = ""; profit_factor = ""; max_drawdown_pct = ""; win_rate = ""; cagr = ""; sortino = ""; yearly_pass = "SKIPPED"; yearly_detail = "config_error"
            })
        continue
    }

    $mFull = $null
    try {
        $rawFull = Invoke-Backtest -Strategy "CryptoV11" -Timerange $fullSampleRange -ConfigDocker $cfgDocker -StrategyPath $CryptoV11StrategyPath
        $mFull = Parse-BacktestOutput $rawFull
    }
    catch {
        Write-Host "  -> full-sample FAILED: $_" -ForegroundColor Red
        "`"$pair`",,,,,,,,,SKIPPED,`"docker_error`"" | Out-File $pairScreenCsv -Append -Encoding utf8
        $pairRankings.Add([PSCustomObject]@{
                pair = $pair; trades = ""; tot_profit_pct = ""; sharpe = ""; profit_factor = ""; max_drawdown_pct = ""; win_rate = ""; cagr = ""; sortino = ""; yearly_pass = "SKIPPED"; yearly_detail = "docker_error"
            })
        continue
    }

    $t0 = [int]$mFull.trades
    $sh0 = [double]$mFull.sharpe
    $pf0 = [double]$mFull.pf
    $pr0 = [double]$mFull.totProfitPct
    $dd0 = $mFull.maxDD
    $wr0 = $mFull.winRate
    $cg0 = $mFull.cagr
    $so0 = $mFull.sortino

    Write-Host "  -> Full: Trades=$t0 Sharpe=$sh0 PF=$pf0 Profit=$pr0%" -ForegroundColor Cyan

    $yearlyPassStr = "SKIPPED"
    $yearlyDetail = ""
    $runYearly = ($sh0 -gt 0 -and $pr0 -gt 0 -and $t0 -gt 50)

    if ($runYearly) {
        $strRows = [System.Collections.Generic.List[object]]::new()
        $detailParts = [System.Collections.Generic.List[string]]::new()

        foreach ($p in $yearlyPeriods) {
            try {
                $rawY = Invoke-Backtest -Strategy "CryptoV11" -Timerange $p.range -ConfigDocker $cfgDocker -StrategyPath $CryptoV11StrategyPath
                $mY = Parse-BacktestOutput $rawY
            }
            catch {
                Write-Host "  -> yearly $($p.year) FAILED: $_" -ForegroundColor Red
                continue
            }
            $pseudo = [PSCustomObject]@{
                year           = "$($p.year)"
                trades         = $mY.trades
                tot_profit_pct = $mY.totProfitPct
                sharpe         = $mY.sharpe
                profit_factor  = $mY.pf
            }
            $strRows.Add($pseudo)

            $pp = [double]$mY.totProfitPct
            $ppSign = if ($pp -ge 0) { "+" } else { "" }
            $detailParts.Add("$($p.year):${ppSign}$pp%/$($mY.sharpe)")
        }
        $yearlyDetail = ($detailParts -join " ")
        $evY = Test-YearlySurvivor -Rows $strRows
        if ($evY.ok) {
            $yearlyPassStr = "PASS"
            $pairYearlyPassCount++
        }
        else {
            $yearlyPassStr = "FAIL"
            $pairYearlyFailCount++
            $yearlyDetail = "$yearlyDetail | $($evY.reason)"
        }
    }
    else {
        $pairYearlySkippedCount++
    }

    $line = "`"$pair`",$t0,$pr0,$sh0,$pf0,$dd0,$wr0,$cg0,$so0,$yearlyPassStr,`"$($yearlyDetail -replace '"','""')`""
    $line | Out-File $pairScreenCsv -Append -Encoding utf8

    $pairRankings.Add([PSCustomObject]@{
            pair             = $pair
            trades           = "$t0"
            tot_profit_pct   = "$pr0"
            sharpe           = "$sh0"
            profit_factor    = "$pf0"
            max_drawdown_pct = "$dd0"
            win_rate         = "$wr0"
            cagr             = "$cg0"
            sortino          = "$so0"
            yearly_pass      = $yearlyPassStr
            yearly_detail    = $yearlyDetail
        })
}

Write-Host ""
Write-Host "NEW PAIRS RANKED BY SHARPE (full-sample)" -ForegroundColor Magenta
$ranked = @($pairRankings | Sort-Object {
        $sx = 0.0
        if (-not [double]::TryParse("$($_.sharpe)", [ref]$sx)) { $sx = [double]::NegativeInfinity }
        $sx
    } -Descending)
$ranked | Format-Table -AutoSize pair, trades, tot_profit_pct, sharpe, profit_factor, max_drawdown_pct, yearly_pass

# ========== Final summary ==========
$pipelineEnd = Get-Date
$dur = $pipelineEnd - $pipelineStart

Write-Host ""
Write-PhaseBanner "V5 PIPELINE COMPLETE"
Write-Host ("Total wall time: {0}" -f $dur.ToString('hh\:mm\:ss')) -ForegroundColor Green
Write-Host ""
Write-Host "Phase 0: downloads ok=$dlOk fail=$dlFail"
Write-Host "Stage 1: full-sample -> $resultsCsv"
Write-Host "Stage 1.5: gate -> $($phase1Candidates.Count) candidates"
Write-Host "Stage 2: yearly -> $yearlyCsv  (pass $stage2Pass / fail $stage2Fail)"
Write-Host "Stage 3: walk-forward -> $wfCsv  (pass $stage3Pass / fail $stage3Fail)"
Write-Host "Pair screening -> $pairScreenCsv"
Write-Host ""

$sbSummary = New-Object System.Text.StringBuilder
[void]$sbSummary.AppendLine("V5 Pipeline Summary")
[void]$sbSummary.AppendLine("===================")
[void]$sbSummary.AppendLine("Started:  $pipelineStart")
[void]$sbSummary.AppendLine("Ended:    $pipelineEnd")
[void]$sbSummary.AppendLine("Duration: $($dur.ToString('hh\:mm\:ss'))")
[void]$sbSummary.AppendLine("")
[void]$sbSummary.AppendLine("Phase 0 (download): ok=$dlOk failed=$dlFail")
[void]$sbSummary.AppendLine("Stage 1:   completed_new=$s1Completed failed=$s1Failed resume_skipped=$s1Skipped")
[void]$sbSummary.AppendLine("Stage 1.5: candidates=$($phase1Candidates.Count)")
[void]$sbSummary.AppendLine("Stage 2:   pass=$stage2Pass fail=$stage2Fail")
[void]$sbSummary.AppendLine("Stage 3:   pass=$stage3Pass fail=$stage3Fail")
[void]$sbSummary.AppendLine("")
[void]$sbSummary.AppendLine("Pair screening (CryptoV11):")
[void]$sbSummary.AppendLine("  yearly PASS=$pairYearlyPassCount FAIL=$pairYearlyFailCount SKIPPED(full-sample gate)=$pairYearlySkippedCount")
[void]$sbSummary.AppendLine("  ranked by Sharpe:")
foreach ($r in $ranked) {
    [void]$sbSummary.AppendLine(("  {0,-22} Sharpe={1,8} PF={2,6} Trades={3,5} Profit%={4,10} Yearly={5}" -f $r.pair, $r.sharpe, $r.profit_factor, $r.trades, $r.tot_profit_pct, $r.yearly_pass))
}
$sbSummary.ToString() | Out-File $summaryFile -Encoding utf8

Write-Host "Summary written: $summaryFile" -ForegroundColor Cyan
