#!/usr/bin/env python3
"""
V7 Stage 3 — Walk-Forward for 18 Stage 2 survivors.
Uses fixed text parser (box-drawing safe). No JSON extraction.
"""
import csv, json, os, re, subprocess, sys, time
from pathlib import Path

WORK_DIR = Path(__file__).resolve().parent.parent.parent
os.chdir(WORK_DIR)

DOCKER_IMAGE = "freqtradeorg/freqtrade:stable"
STRATEGY_PATH = "/freqtrade/user_data/strategies/experiments_v7"
CONFIG_PATH = "/freqtrade/user_data/config_backtest.json"

GATES_FILE = WORK_DIR / "user_data" / "configs" / "experiment_gates.json"
RESULTS_DIR = WORK_DIR / "user_data" / "experiment_results"
WF_CSV = RESULTS_DIR / "v7_walkforward.csv"
RESULTS_CSV = RESULTS_DIR / "v7_results.csv"

R = "\033[0;31m"; G = "\033[0;32m"; Y = "\033[1;33m"; C = "\033[0;36m"; M = "\033[0;35m"; NC = "\033[0m"

with open(GATES_FILE) as f:
    gates = json.load(f)
S3 = gates["stage3"]
wf_windows = S3["walkforward_windows"]

SURVIVORS = [
    "V7_G1_P001", "V7_G1_P002", "V7_G1_P003", "V7_G1_P004",
    "V7_G1_P005", "V7_G1_P006", "V7_G1_P007", "V7_G1_P008",
    "V7_G1_P009", "V7_G1_P010", "V7_G1_P011", "V7_G1_P012",
    "V7_G2_P011", "V7_G13_P004", "V7_G13_P007", "V7_G13_P008",
    "V7_G14_P004", "V7_G14_P006",
]

def sf(v, d=0.0):
    try: return float(v)
    except: return d

def load_csv(p):
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def append_csv(p, row):
    with open(p, "a", encoding="utf-8") as f:
        f.write(row + "\n")

# Load strategy info from results CSV
results_map = {}
for r in load_csv(RESULTS_CSV):
    results_map[r["strategy"]] = r

def run_backtest(strategy, timerange):
    cmd = [
        "docker", "run", "--rm",
        "-v", "./user_data:/freqtrade/user_data",
        DOCKER_IMAGE, "backtesting",
        "--config", CONFIG_PATH,
        "--strategy", strategy,
        "--strategy-path", STRATEGY_PATH,
        "--timerange", timerange,
        "--cache", "none",
        "--starting-balance", "1000",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return ""
    except Exception as e:
        print(f"  -> ERROR: {e}")
        return ""

def parse_text(output):
    """Parse backtest metrics from text output (box-drawing safe)."""
    def grab(pattern, default="0"):
        m = re.search(pattern, output, re.MULTILINE)
        return m.group(1) if m else default
    return {
        "trades": grab(r'Total/Daily Avg Trades[^0-9]*(\d+)\s+/'),
        "tot_pct": grab(r'Total profit %[^0-9\-]*([\-\d\.]+)%'),
        "sharpe": grab(r'Sharpe\s+[^0-9\-]*([\-\d\.]+)'),
        "pf": grab(r'Profit factor\s+[^0-9\-]*([\-\d\.]+)'),
        "maxdd": grab(r'Absolute drawdown.*?\(([\d\.]+)%\)'),
        "cagr": grab(r'CAGR %\s+[^0-9\-]*([\-\d\.]+)'),
        "sortino": grab(r'Sortino\s+[^0-9\-]*([\-\d\.]+)'),
    }

# ── Init CSV ────────────────────────────────────────────────────────────
S3_HEADER = "strategy,group,name,window,phase,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,cagr,sortino"
if not WF_CSV.exists() or WF_CSV.stat().st_size < 50:
    WF_CSV.write_text(S3_HEADER + "\n", encoding="utf-8")

done_wf = set()
for r in load_csv(WF_CSV):
    done_wf.add(f'{r.get("strategy","")}|{r.get("window","")}|{r.get("phase","")}')

total = len(SURVIVORS) * len(wf_windows) * 2
print(f"\n{M}{'='*60}")
print(f" STAGE 3 — Walk-Forward ({len(SURVIVORS)} x {len(wf_windows)} windows x 2 = {total} runs)")
print(f"{'='*60}{NC}\n")
print(f"{Y}Resume: {len(done_wf)} rows already done{NC}")

idx = 0
start = time.time()

for surv in SURVIVORS:
    info = results_map.get(surv, {})
    group = info.get("group", "")
    name = info.get("name", "")

    for w in wf_windows:
        wname = w["name"]
        for phase in ["train", "test"]:
            idx += 1
            tr = w["train"] if phase == "train" else w["test"]
            key = f"{surv}|{wname}|{phase}"
            if key in done_wf:
                continue

            elapsed = time.time() - start
            eta = round(elapsed / max(idx - len(done_wf), 1) * (total - idx) / 60) if idx > len(done_wf) else "?"
            pct = round(idx / total * 100)
            print(f"{C}[{idx}/{total}] ({pct}%) {surv} {wname} {phase} (ETA ~{eta}min){NC}")

            raw = run_backtest(surv, tr)
            m = parse_text(raw) if raw.strip() else {
                "trades": "0", "tot_pct": "0", "sharpe": "0",
                "pf": "0", "maxdd": "0", "cagr": "0", "sortino": "0"
            }

            append_csv(WF_CSV,
                f'{surv},{group},"{name}",{wname},{phase},{tr},{m["trades"]},'
                f'{m["tot_pct"]},{m["sharpe"]},{m["pf"]},{m["maxdd"]},'
                f'{m["cagr"]},{m["sortino"]}')

            color = G if sf(m["sharpe"]) > 0 else R
            print(f'{color}  -> Sharpe={m["sharpe"]} PF={m["pf"]} Profit={m["tot_pct"]}% Trades={m["trades"]}{NC}')

# ── Evaluate Walk-Forward Gates ─────────────────────────────────────────
print(f"\n{Y}Evaluating walk-forward gates...{NC}")
all_wf = load_csv(WF_CSV)
s3_pass = []

for surv in SURVIVORS:
    ok = True
    reason = "ok"
    for w in wf_windows:
        test_rows = [r for r in all_wf if r.get("strategy") == surv and r.get("window") == w["name"] and r.get("phase") == "test"]
        train_rows = [r for r in all_wf if r.get("strategy") == surv and r.get("window") == w["name"] and r.get("phase") == "train"]
        if not test_rows or not train_rows:
            ok = False; reason = f'missing {w["name"]}'; break
        if sf(test_rows[0].get("sharpe")) <= 0:
            ok = False; reason = f'{w["name"]} test Sharpe={test_rows[0].get("sharpe")} <= 0'; break
        tpf = sf(test_rows[0].get("profit_factor"))
        trpf = sf(train_rows[0].get("profit_factor"))
        if trpf > 0 and tpf < trpf * 0.8:
            ok = False; reason = f'{w["name"]} PF decay ({tpf:.2f} vs train {trpf:.2f})'; break

    if ok:
        print(f"{G}[PASS WF] {surv}{NC}")
        s3_pass.append(surv)
    else:
        print(f"{R}[FAIL WF] {surv} :: {reason}{NC}")

elapsed = int(time.time() - start)
h, remainder = divmod(elapsed, 3600)
mins, secs = divmod(remainder, 60)

print(f"\n{M}{'='*60}")
print(f" STAGE 3 RESULTS")
print(f"{'='*60}{NC}")
print(f"Duration: {h:02d}:{mins:02d}:{secs:02d}")
print(f"Input: {len(SURVIVORS)} survivors")
print(f"Pass:  {len(s3_pass)}")
print(f"Fail:  {len(SURVIVORS) - len(s3_pass)}")
if s3_pass:
    print(f"\n{G}FINAL SURVIVORS:{NC}")
    for s in s3_pass:
        info = results_map.get(s, {})
        print(f"  {s:<22} Sharpe={info.get('sharpe','?')}  PF={info.get('profit_factor','?')}  DD={info.get('max_drawdown_pct','?')}%  -- {info.get('name','')}")
else:
    print(f"\n{Y}No strategies survived all 3 stages.{NC}")

# Save summary
summary = f"""V7 Stage 3 Summary
==================
Duration: {h:02d}:{mins:02d}:{secs:02d}
Stage 2 survivors: {len(SURVIVORS)}
Stage 3 pass: {len(s3_pass)}
Stage 3 fail: {len(SURVIVORS) - len(s3_pass)}
Final: {', '.join(s3_pass) if s3_pass else 'none'}
"""
(RESULTS_DIR / "v7_pipeline_summary.txt").write_text(summary, encoding="utf-8")

# Run analysis
analyze = WORK_DIR / "user_data" / "scripts" / "analyze_v7.py"
if analyze.exists():
    print(f"\n{Y}Running analyze_v7.py...{NC}")
    try:
        subprocess.run([sys.executable, str(analyze)], check=True)
        print(f"{G}Analysis saved to v7_analysis.md{NC}")
    except:
        print(f"{Y}Analysis script failed{NC}")

print(f"\n{G}Pipeline complete!{NC}")
