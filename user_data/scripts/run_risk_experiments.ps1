$manifestPath = "user_data/scripts/risk_experiment_manifest.json"
$resultsCsv   = "user_data/scripts/risk_results.csv"
$strategyDir  = "/freqtrade/user_data/strategies/experiments"

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

"strategy,group,params,trades,avg_profit_pct,tot_profit_usdt,tot_profit_pct,sharpe,pf,max_drawdown_pct,win_rate,cagr,sortino" | Out-File $resultsCsv -Encoding utf8

$total = $manifest.Count
$i = 0

foreach ($exp in $manifest) {
    $i++
    $strategy = $exp.name
    $group    = $exp.group
    $params   = $exp.params

    Write-Host "[$i/$total] Running $strategy ($group) ..." -ForegroundColor Cyan

    $rawOutput = docker run --rm `
        -v "./user_data:/freqtrade/user_data" `
        freqtradeorg/freqtrade:stable backtesting `
        --config /freqtrade/user_data/config_backtest.json `
        --strategy $strategy `
        --strategy-path $strategyDir `
        --timerange 20200101-20260401 `
        --cache none `
        --starting-balance 1000 2>&1

    $output = $rawOutput -join "`n"

    $trades = "0"; $avgProfit = "0"; $totUsdt = "0"; $totPct = "0"
    $sharpe = "0"; $pf = "0"; $dd = "0"; $winRate = "0"; $cagr = "0"; $sortino = "0"

    if ($output -match "Total/Daily Avg Trades\s+.?\s+(\d+)") { $trades = $Matches[1] }
    if ($output -match "Total profit %\s+.?\s+([\d\.\-]+)") { $totPct = $Matches[1] }
    if ($output -match "Absolute profit\s+.?\s+([\d\.\-]+)") { $totUsdt = $Matches[1] }
    if ($output -match "Sharpe\s+.?\s+([\d\.\-]+)") { $sharpe = $Matches[1] }
    if ($output -match "Profit factor\s+.?\s+([\d\.\-]+)") { $pf = $Matches[1] }
    if ($output -match "Absolute drawdown\s+[^│]+.?\s*[^(]*\(([\d\.]+)%\)") { $dd = $Matches[1] }
    if ($output -match "CAGR %\s+.?\s+([\d\.\-]+)") { $cagr = $Matches[1] }
    if ($output -match "Sortino\s+.?\s+([\d\.\-]+)") { $sortino = $Matches[1] }

    if ($output -match "TOTAL\s+.\s+\d+\s+.\s+([\d\.\-]+)\s+.") { $avgProfit = $Matches[1] }
    if ($output -match "Win%\s*.\s*$" -or $output -match "(\d+\.\d+)\s+.?\s*$") {
        if ($output -match "TOTAL.*?(\d+\.\d)\s*│?\s*$") { $winRate = $Matches[1] }
    }
    if ($output -match "TOTAL\s+│\s+\d+\s+│\s+[\d\.\-]+\s+│.*?(\d+\.\d)\s+│?\s*$") {
        # noop, already matched
    }

    $line = "$strategy,$group,$params,$trades,$avgProfit,$totUsdt,$totPct,$sharpe,$pf,$dd,$winRate,$cagr,$sortino"
    $line | Out-File $resultsCsv -Append -Encoding utf8

    Write-Host "  -> Trades=$trades Sharpe=$sharpe PF=$pf Profit=$totPct% DD=$dd% CAGR=$cagr%" -ForegroundColor Green
}

Write-Host "`n=== All $total experiments completed ===" -ForegroundColor Yellow
Write-Host "Results saved to $resultsCsv"
