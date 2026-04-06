$manifestPath = "user_data/scripts/risk_experiment_manifest.json"
$resultsCsv   = "user_data/scripts/risk_results.csv"
$strategyDir  = "/freqtrade/user_data/strategies/risk_exp"

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

"strategy,group,params,trades,tot_profit_pct,sharpe,pf,max_drawdown_pct,cagr,sortino" | Out-File $resultsCsv -Encoding utf8

$total = $manifest.Count
$i = 0

foreach ($exp in $manifest) {
    $i++
    $strategy = $exp.name
    $group    = $exp.group
    $params   = $exp.params -replace ",", ";"

    Write-Host "[$i/$total] $strategy ($group) ..." -ForegroundColor Cyan

    $rawOutput = docker run --rm `
        -v "./user_data:/freqtrade/user_data" `
        freqtradeorg/freqtrade:stable backtesting `
        --config /freqtrade/user_data/config_backtest.json `
        --strategy $strategy `
        --strategy-path $strategyDir `
        --timerange 20200101-20260401 `
        --cache none `
        --starting-balance 1000 2>&1

    $output = $rawOutput | Out-String

    $trades = "N/A"; $totPct = "N/A"; $sharpe = "N/A"; $pf = "N/A"
    $dd = "N/A"; $cagr = "N/A"; $sortino = "N/A"

    if ($output -match "Total/Daily Avg Trades\s+\S+\s+(\d+)") { $trades = $Matches[1] }
    if ($output -match "Total profit %\s+\S+\s+([\d\.\-]+)") { $totPct = $Matches[1] }
    if ($output -match "(?m)^\s*Sharpe\s+\S+\s+([\d\.\-]+)") { $sharpe = $Matches[1] }
    if ($output -match "Profit factor\s+\S+\s+([\d\.\-]+)") { $pf = $Matches[1] }
    if ($output -match "CAGR %\s+\S+\s+([\d\.\-]+)") { $cagr = $Matches[1] }
    if ($output -match "Sortino\s+\S+\s+([\d\.\-]+)") { $sortino = $Matches[1] }
    if ($output -match "\((\d+\.\d+)%\)") { $dd = $Matches[1] }

    $line = "$strategy,$group,$params,$trades,$totPct,$sharpe,$pf,$dd,$cagr,$sortino"
    $line | Out-File $resultsCsv -Append -Encoding utf8

    Write-Host "  Trades=$trades Sharpe=$sharpe PF=$pf Profit=${totPct}% DD=${dd}% CAGR=${cagr}%" -ForegroundColor Green
}

Write-Host "`n=== Done: $total experiments ===" -ForegroundColor Yellow
