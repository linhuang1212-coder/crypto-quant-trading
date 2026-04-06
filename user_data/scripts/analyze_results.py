"""
Experiment Results Analyzer
读取 all_results.csv，生成完整分析报告。
你醒来后运行这个脚本即可看到所有结论。

Usage:
    python user_data/scripts/analyze_results.py
"""
import csv
import os
import sys
from collections import defaultdict

RESULTS_CSV = os.path.join(os.path.dirname(os.path.dirname(__file__)), "experiment_results", "all_results.csv")
REPORT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "experiment_results", "analysis_report.md")

BASELINE = {
    "strategy": "CryptoV10",
    "trades": 1179, "sharpe": 0.77, "pf": 1.23,
    "tot_profit_pct": 425.0, "max_drawdown_pct": 21.0, "win_rate": 33.4,
    "cagr": 30.4,
}


def load_results():
    results = []
    with open(RESULTS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("trades") == "FAILED":
                row["_failed"] = True
                results.append(row)
                continue
            try:
                row["trades"] = int(row["trades"])
                for key in ["avg_profit_pct", "tot_profit_usdt", "tot_profit_pct",
                            "sharpe", "profit_factor", "max_drawdown_pct", "win_rate",
                            "cagr", "sortino"]:
                    row[key] = float(row.get(key, 0) or 0)
                row["_failed"] = False
            except (ValueError, TypeError):
                row["_failed"] = True
            results.append(row)
    return results


def fmt(val, decimals=2):
    if isinstance(val, float):
        return f"{val:.{decimals}f}"
    return str(val)


def generate_report(results):
    lines = []
    lines.append("# 8-Hour Experiment Analysis Report")
    lines.append(f"> Generated from {len(results)} experiments\n")

    valid = [r for r in results if not r["_failed"]]
    failed = [r for r in results if r["_failed"]]

    lines.append(f"**Total**: {len(results)} | **Success**: {len(valid)} | **Failed**: {len(failed)}\n")

    # Baseline comparison
    lines.append("## Baseline (CryptoV10)")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Sharpe | {BASELINE['sharpe']} |")
    lines.append(f"| Profit Factor | {BASELINE['pf']} |")
    lines.append(f"| Total Profit | {BASELINE['tot_profit_pct']}% |")
    lines.append(f"| Max Drawdown | {BASELINE['max_drawdown_pct']}% |")
    lines.append(f"| Win Rate | {BASELINE['win_rate']}% |")
    lines.append(f"| CAGR | {BASELINE['cagr']}% |")
    lines.append("")

    # ── TOP 20 by Sharpe ──
    by_sharpe = sorted(valid, key=lambda x: x["sharpe"], reverse=True)[:20]
    lines.append("## Top 20 by Sharpe Ratio")
    lines.append("| # | Strategy | Group | Sharpe | PF | Profit% | DD% | WinRate | Trades |")
    lines.append("|---|----------|-------|--------|-----|---------|-----|---------|--------|")
    for i, r in enumerate(by_sharpe, 1):
        better = " **" if r["sharpe"] > BASELINE["sharpe"] else ""
        end = "**" if better else ""
        lines.append(f"| {i} | {r['name']} | {r['group']} | {better}{fmt(r['sharpe'])}{end} | {fmt(r['profit_factor'])} | {fmt(r['tot_profit_pct'],1)} | {fmt(r['max_drawdown_pct'],1)} | {fmt(r['win_rate'],1)} | {r['trades']} |")
    lines.append("")

    # ── TOP 20 by Profit Factor ──
    by_pf = sorted(valid, key=lambda x: x["profit_factor"], reverse=True)[:20]
    lines.append("## Top 20 by Profit Factor")
    lines.append("| # | Strategy | Group | PF | Sharpe | Profit% | DD% | WinRate | Trades |")
    lines.append("|---|----------|-------|-----|--------|---------|-----|---------|--------|")
    for i, r in enumerate(by_pf, 1):
        better = " **" if r["profit_factor"] > BASELINE["pf"] else ""
        end = "**" if better else ""
        lines.append(f"| {i} | {r['name']} | {r['group']} | {better}{fmt(r['profit_factor'])}{end} | {fmt(r['sharpe'])} | {fmt(r['tot_profit_pct'],1)} | {fmt(r['max_drawdown_pct'],1)} | {fmt(r['win_rate'],1)} | {r['trades']} |")
    lines.append("")

    # ── TOP 10 by Risk-Adjusted (Profit / MaxDD ratio) ──
    for r in valid:
        r["profit_dd_ratio"] = r["tot_profit_pct"] / max(r["max_drawdown_pct"], 0.1)
    by_ratio = sorted(valid, key=lambda x: x["profit_dd_ratio"], reverse=True)[:10]
    lines.append("## Top 10 by Profit/Drawdown Ratio")
    lines.append("| # | Strategy | Group | P/DD | Sharpe | PF | Profit% | DD% |")
    lines.append("|---|----------|-------|------|--------|-----|---------|-----|")
    for i, r in enumerate(by_ratio, 1):
        lines.append(f"| {i} | {r['name']} | {r['group']} | {fmt(r['profit_dd_ratio'],1)} | {fmt(r['sharpe'])} | {fmt(r['profit_factor'])} | {fmt(r['tot_profit_pct'],1)} | {fmt(r['max_drawdown_pct'],1)} |")
    lines.append("")

    # ── WORST 10 (negative Sharpe / avoid) ──
    by_worst = sorted(valid, key=lambda x: x["sharpe"])[:10]
    lines.append("## Worst 10 (Avoid These)")
    lines.append("| # | Strategy | Group | Sharpe | PF | Profit% | DD% | Trades |")
    lines.append("|---|----------|-------|--------|-----|---------|-----|--------|")
    for i, r in enumerate(by_worst, 1):
        lines.append(f"| {i} | {r['name']} | {r['group']} | {fmt(r['sharpe'])} | {fmt(r['profit_factor'])} | {fmt(r['tot_profit_pct'],1)} | {fmt(r['max_drawdown_pct'],1)} | {r['trades']} |")
    lines.append("")

    # ── Group-level analysis ──
    groups = defaultdict(list)
    for r in valid:
        groups[r["group"]].append(r)

    lines.append("## Group-Level Summary")
    lines.append("| Group | Count | Best Sharpe | Avg Sharpe | Best PF | Avg PF | Best Profit% |")
    lines.append("|-------|-------|-------------|------------|---------|--------|--------------|")
    for g, rs in sorted(groups.items()):
        best_s = max(r["sharpe"] for r in rs)
        avg_s = sum(r["sharpe"] for r in rs) / len(rs)
        best_pf = max(r["profit_factor"] for r in rs)
        avg_pf = sum(r["profit_factor"] for r in rs) / len(rs)
        best_p = max(r["tot_profit_pct"] for r in rs)
        lines.append(f"| {g} | {len(rs)} | {fmt(best_s)} | {fmt(avg_s)} | {fmt(best_pf)} | {fmt(avg_pf)} | {fmt(best_p,1)} |")
    lines.append("")

    # ── Parameter sensitivity for param_scan ──
    param_groups = defaultdict(list)
    for r in valid:
        if r["group"] == "param_scan":
            name = r["name"]
            if "=" in name and "_" not in name.split("=")[0].replace("_", "", 1):
                param_name = name.split("=")[0]
                param_groups[param_name].append(r)

    if param_groups:
        lines.append("## Parameter Sensitivity Analysis (CryptoV10 variants)")
        for param_name, rs in sorted(param_groups.items()):
            rs_sorted = sorted(rs, key=lambda x: x["sharpe"], reverse=True)
            lines.append(f"\n### {param_name}")
            lines.append("| Value | Sharpe | PF | Profit% | DD% | Trades | vs Baseline |")
            lines.append("|-------|--------|-----|---------|-----|--------|-------------|")
            for r in rs_sorted:
                val = r["name"].split("=")[1] if "=" in r["name"] else r["name"]
                delta_s = r["sharpe"] - BASELINE["sharpe"]
                sign = "+" if delta_s >= 0 else ""
                lines.append(f"| {val} | {fmt(r['sharpe'])} | {fmt(r['profit_factor'])} | {fmt(r['tot_profit_pct'],1)} | {fmt(r['max_drawdown_pct'],1)} | {r['trades']} | Sharpe {sign}{fmt(delta_s)} |")
        lines.append("")

    # ── Strategies that beat baseline ──
    beaters = [r for r in valid if r["sharpe"] > BASELINE["sharpe"]
               and r["profit_factor"] > BASELINE["pf"]]
    beaters.sort(key=lambda x: x["sharpe"], reverse=True)

    lines.append("## Strategies That Beat Baseline (Sharpe > 0.77 AND PF > 1.23)")
    if beaters:
        lines.append("| Strategy | Group | Sharpe | PF | Profit% | DD% | WinRate | Trades |")
        lines.append("|----------|-------|--------|-----|---------|-----|---------|--------|")
        for r in beaters:
            lines.append(f"| {r['name']} | {r['group']} | {fmt(r['sharpe'])} | {fmt(r['profit_factor'])} | {fmt(r['tot_profit_pct'],1)} | {fmt(r['max_drawdown_pct'],1)} | {fmt(r['win_rate'],1)} | {r['trades']} |")
    else:
        lines.append("*None found. Baseline CryptoV10 remains the best.*")
    lines.append("")

    # ── New strategy prototypes comparison ──
    new_strategies = [r for r in valid if r["group"] in ("bollinger_band", "macd", "keltner", "ema_cross", "rsi_trend")]
    if new_strategies:
        lines.append("## New Strategy Prototypes (Non-Donchian)")
        lines.append("| Strategy | Type | Sharpe | PF | Profit% | DD% | WinRate | Trades | Viable? |")
        lines.append("|----------|------|--------|-----|---------|-----|---------|--------|---------|")
        for r in sorted(new_strategies, key=lambda x: x["sharpe"], reverse=True):
            viable = "YES" if r["sharpe"] > 0.3 and r["profit_factor"] > 1.1 and r["trades"] > 50 else "NO"
            lines.append(f"| {r['name']} | {r['group']} | {fmt(r['sharpe'])} | {fmt(r['profit_factor'])} | {fmt(r['tot_profit_pct'],1)} | {fmt(r['max_drawdown_pct'],1)} | {fmt(r['win_rate'],1)} | {r['trades']} | {viable} |")
    lines.append("")

    # ── Conclusions ──
    lines.append("## Key Conclusions")
    lines.append("")

    if beaters:
        lines.append(f"1. **{len(beaters)} strategies beat the baseline** on both Sharpe and PF.")
        best = beaters[0]
        lines.append(f"   Best: **{best['name']}** (Sharpe {fmt(best['sharpe'])}, PF {fmt(best['profit_factor'])})")
    else:
        lines.append("1. **No strategy beat the baseline** on both Sharpe and PF simultaneously.")
        lines.append("   CryptoV10 with current parameters remains optimal.")

    viable_new = [r for r in new_strategies if r.get("sharpe", 0) > 0.3 and r.get("profit_factor", 0) > 1.1]
    if viable_new:
        lines.append(f"2. **{len(viable_new)} new strategy prototypes are viable** for further development:")
        for r in viable_new[:3]:
            lines.append(f"   - {r['name']} (Sharpe {fmt(r['sharpe'])}, PF {fmt(r['profit_factor'])})")
    else:
        lines.append("2. **No new strategy prototypes showed viability.** Donchian breakout remains superior.")

    lines.append("")
    lines.append("---")
    lines.append("*Report generated by analyze_results.py*")

    report = "\n".join(lines)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    if not os.path.exists(RESULTS_CSV):
        print(f"Error: {RESULTS_CSV} not found. Run experiments first.")
        sys.exit(1)
    results = load_results()
    generate_report(results)
