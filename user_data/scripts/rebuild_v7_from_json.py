#!/usr/bin/env python3
"""
Rebuild v7_results.csv from Freqtrade JSON backtest result files.
For strategies missing from JSON (all had 0 trades), use existing CSV data.
"""
import csv, json, zipfile, os, glob, sys
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = WORK_DIR / "user_data" / "experiment_results"
BT_DIR = WORK_DIR / "user_data" / "backtest_results"
MANIFEST = WORK_DIR / "user_data" / "experiment_manifest_v7.json"
OLD_CSV = RESULTS_DIR / "v7_results.csv"
NEW_CSV = RESULTS_DIR / "v7_results_fixed.csv"

with open(MANIFEST) as f:
    manifest = json.load(f)
manifest_map = {e["strategy"]: e for e in manifest}

# Extract all V7 strategies from JSON zip files
json_data = {}
for zf_path in sorted(glob.glob(str(BT_DIR / "*.zip"))):
    try:
        with zipfile.ZipFile(zf_path) as z:
            json_files = [n for n in z.namelist() if n.endswith(".json") and "config" not in n]
            for jf_name in json_files:
                with z.open(jf_name) as jf:
                    data = json.load(jf)
                    for sname, sd in data.get("strategy", {}).items():
                        if not sname.startswith("V7_"):
                            continue
                        trades = sd.get("total_trades", 0)
                        winning = sd.get("winning_trades", 0)
                        losing = sd.get("losing_trades", 0)
                        wr = round(winning / (winning + losing) * 100, 2) if (winning + losing) > 0 else 0
                        profit_total = sd.get("profit_total", 0) * 100
                        profit_abs = sd.get("profit_total_abs", 0)
                        avg_pct = round(profit_total / trades, 4) if trades > 0 else 0
                        dd = round(sd.get("max_drawdown_account", 0) * 100, 2)

                        json_data[sname] = {
                            "trades": trades,
                            "avg_profit_pct": avg_pct,
                            "tot_profit_usdt": round(profit_abs, 3),
                            "tot_profit_pct": round(profit_total, 2),
                            "sharpe": round(sd.get("sharpe", 0), 2),
                            "profit_factor": round(sd.get("profit_factor", 0) or 0, 2),
                            "max_drawdown_pct": dd,
                            "win_rate": wr,
                            "cagr": round((sd.get("cagr", 0) or 0) * 100, 2),
                            "sortino": round(sd.get("sortino", 0) or 0, 2),
                        }
    except Exception as e:
        print(f"Error reading {zf_path}: {e}", file=sys.stderr)

print(f"Extracted {len(json_data)} V7 strategies from JSON files")

# Read old CSV for strategies without JSON data
old_rows = {}
if OLD_CSV.exists():
    with open(OLD_CSV, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            old_rows[r["strategy"]] = r

# Build new CSV
HEADER = "strategy,group,name,trades,avg_profit_pct,tot_profit_usdt,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino,params"
rows = []

for exp in manifest:
    sname = exp["strategy"]
    group = exp["group"]
    name = exp["name"]
    params = json.dumps(exp.get("params", {}), ensure_ascii=False).replace('"', '""')

    if sname in json_data:
        d = json_data[sname]
        row = (f'{sname},{group},"{name}",{d["trades"]},{d["avg_profit_pct"]},'
               f'{d["tot_profit_usdt"]},{d["tot_profit_pct"]},{d["sharpe"]},'
               f'{d["profit_factor"]},{d["max_drawdown_pct"]},{d["win_rate"]},'
               f'{d["cagr"]},{d["sortino"]},"{params}"')
        rows.append(row)
    elif sname in old_rows:
        r = old_rows[sname]
        row = (f'{sname},{group},"{name}",{r.get("trades",0)},{r.get("avg_profit_pct",0)},'
               f'{r.get("tot_profit_usdt",0)},{r.get("tot_profit_pct",0)},{r.get("sharpe",0)},'
               f'{r.get("profit_factor",0)},{r.get("max_drawdown_pct",0)},{r.get("win_rate",0)},'
               f'{r.get("cagr",0)},{r.get("sortino",0)},"{params}"')
        rows.append(row)
    else:
        row = f'{sname},{group},"{name}",0,0,0,0,0,0,0,0,0,0,"{params}"'
        rows.append(row)

with open(NEW_CSV, "w", encoding="utf-8") as f:
    f.write(HEADER + "\n")
    for r in rows:
        f.write(r + "\n")

print(f"Wrote {len(rows)} rows to {NEW_CSV}")

# Show top strategies by Sharpe
print("\n=== Top 15 by Sharpe (from JSON) ===")
by_sharpe = sorted(json_data.items(), key=lambda x: x[1]["sharpe"], reverse=True)
for sname, d in by_sharpe[:15]:
    minfo = manifest_map.get(sname, {})
    print(f'  {sname:<20} Sharpe={d["sharpe"]:>6.2f}  PF={d["profit_factor"]:>5.2f}  '
          f'Trades={d["trades"]:>5}  DD={d["max_drawdown_pct"]:>5.1f}%  '
          f'Profit={d["tot_profit_pct"]:>8.1f}%  WR={d["win_rate"]}%  '
          f'CAGR={d["cagr"]}%  -- {minfo.get("name","")}')

# Check Stage 1 gate
print("\n=== Stage 1 Gate Check (Sharpe>0.9, PF>1.3, Trades>800, DD<25%) ===")
candidates = []
for sname, d in json_data.items():
    if (d["sharpe"] > 0.9 and d["profit_factor"] > 1.3 and
        d["trades"] > 800 and d["max_drawdown_pct"] < 25.0):
        candidates.append((sname, d))
        minfo = manifest_map.get(sname, {})
        print(f'  PASS: {sname:<20} Sharpe={d["sharpe"]:>6.2f}  PF={d["profit_factor"]:>5.2f}  '
              f'Trades={d["trades"]:>5}  DD={d["max_drawdown_pct"]:>5.1f}%  -- {minfo.get("name","")}')

if not candidates:
    print("  (No candidates pass all gates)")
print(f"\nTotal candidates: {len(candidates)}")
