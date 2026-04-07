#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V7 Experiment Pipeline — 3-stage anti-overfitting
Stage 1: Full-sample screen → Stage 2: Yearly validation → Stage 3: Walk-Forward → Analysis

Usage:
    cd ~/crypto-quant-trading && python3 user_data/scripts/run_experiments_v7.py
"""
import csv
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
WORK_DIR = Path(__file__).resolve().parent.parent.parent
os.chdir(WORK_DIR)

DOCKER_IMAGE = "freqtradeorg/freqtrade:stable"
STRATEGY_PATH = "/freqtrade/user_data/strategies/experiments_v7"
CONFIG_PATH = "/freqtrade/user_data/config_backtest.json"

MANIFEST = WORK_DIR / "user_data" / "experiment_manifest_v7.json"
GATES_FILE = WORK_DIR / "user_data" / "configs" / "experiment_gates.json"
RESULTS_DIR = WORK_DIR / "user_data" / "experiment_results"
RESULTS_CSV = RESULTS_DIR / "v7_results.csv"
YEARLY_CSV = RESULTS_DIR / "v7_yearly.csv"
WF_CSV = RESULTS_DIR / "v7_walkforward.csv"
PROGRESS_FILE = RESULTS_DIR / "v7_progress.txt"
SUMMARY_FILE = RESULTS_DIR / "v7_pipeline_summary.txt"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Colors ─────────────────────────────────────────────────────────────────
R = "\033[0;31m"; G = "\033[0;32m"; Y = "\033[1;33m"; C = "\033[0;36m"; M = "\033[0;35m"; NC = "\033[0m"

def banner(title):
    print(f"\n{M}{'='*60}\n {title}\n{'='*60}{NC}\n")

def cprint(color, msg):
    print(f"{color}{msg}{NC}")

# ── Load config ────────────────────────────────────────────────────────────
with open(MANIFEST) as f:
    manifest = json.load(f)
with open(GATES_FILE) as f:
    gates = json.load(f)

FULL_RANGE = gates["full_sample_timerange"]
S1 = gates["stage1"]
S2 = gates["stage2"]
S3 = gates["stage3"]

# ── Helpers ────────────────────────────────────────────────────────────────
def run_backtest(strategy: str, timerange: str, spath: str = STRATEGY_PATH) -> str:
    cmd = [
        "docker", "run", "--rm",
        "-v", "./user_data:/freqtrade/user_data",
        DOCKER_IMAGE, "backtesting",
        "--config", CONFIG_PATH,
        "--strategy", strategy,
        "--strategy-path", spath,
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


def parse_backtest_from_json(strategy: str) -> dict:
    """Read metrics from the most recent Freqtrade JSON result file for this strategy."""
    import zipfile
    bt_dir = WORK_DIR / "user_data" / "backtest_results"
    best = None
    best_mtime = 0
    for zf_path in bt_dir.glob("*.zip"):
        mt = zf_path.stat().st_mtime
        if mt < best_mtime:
            continue
        try:
            with zipfile.ZipFile(zf_path) as z:
                json_files = [n for n in z.namelist() if n.endswith(".json") and "config" not in n]
                for jf_name in json_files:
                    with z.open(jf_name) as jf:
                        data = json.load(jf)
                        if strategy in data.get("strategy", {}):
                            best = data["strategy"][strategy]
                            best_mtime = mt
        except:
            pass
    if best is None:
        return None
    sd = best
    trades = sd.get("total_trades", 0)
    winning = sd.get("winning_trades", 0)
    losing = sd.get("losing_trades", 0)
    wr = round(winning / (winning + losing) * 100, 2) if (winning + losing) > 0 else 0
    profit_pct = round(sd.get("profit_total", 0) * 100, 2)
    profit_abs = round(sd.get("profit_total_abs", 0), 3)
    avg_profit = str(round(profit_pct / trades, 4)) if trades > 0 else "0"
    dd = round(sd.get("max_drawdown_account", 0) * 100, 2)
    return {
        "trades": str(trades), "avg_profit": avg_profit,
        "tot_usdt": str(profit_abs), "tot_pct": str(profit_pct),
        "sharpe": str(round(sd.get("sharpe", 0), 2)),
        "pf": str(round(sd.get("profit_factor", 0) or 0, 2)),
        "maxdd": str(dd),
        "winrate": str(wr),
        "cagr": str(round((sd.get("cagr", 0) or 0) * 100, 2)),
        "sortino": str(round(sd.get("sortino", 0) or 0, 2)),
    }


def parse_backtest(output: str) -> dict:
    """Fallback: parse metrics from text output (handles box-drawing chars)."""
    def grab(pattern, default="0"):
        m = re.search(pattern, output, re.MULTILINE)
        return m.group(1) if m else default

    trades = grab(r'Total/Daily Avg Trades[^0-9]*([\d]+)\s+/')
    tot_pct = grab(r'Total profit %[^0-9\-]*([\-\d\.]+)%')
    tot_usdt = grab(r'Absolute profit[^0-9\-]*([\-\d\.]+)\s+USDT')
    sharpe = grab(r'Sharpe\s+[^0-9\-]*([\-\d\.]+)')
    sortino = grab(r'Sortino\s+[^0-9\-]*([\-\d\.]+)')
    pf = grab(r'Profit factor\s+[^0-9\-]*([\-\d\.]+)')
    cagr = grab(r'CAGR %\s+[^0-9\-]*([\-\d\.]+)')
    maxdd = grab(r'Absolute drawdown.*?\(([\d\.]+)%\)')
    winrate = grab(r'TOTAL.*?([\d]+\.?\d*)\s*[│|]\s*$', "0")

    try:
        t = int(trades)
        avg_profit = str(round(float(tot_pct) / t, 4)) if t > 0 else "0"
    except:
        avg_profit = "0"

    return {
        "trades": trades, "avg_profit": avg_profit, "tot_usdt": tot_usdt,
        "tot_pct": tot_pct, "sharpe": sharpe, "pf": pf, "maxdd": maxdd,
        "winrate": winrate, "cagr": cagr, "sortino": sortino,
    }


def run_and_parse(strategy: str, timerange: str) -> dict:
    """Run backtest, then extract metrics from JSON (preferred) or text output (fallback)."""
    raw = run_backtest(strategy, timerange)
    result = parse_backtest_from_json(strategy)
    if result and int(result["trades"]) > 0:
        return result
    return parse_backtest(raw) if raw.strip() else {
        "trades": "0", "avg_profit": "0", "tot_usdt": "0", "tot_pct": "0",
        "sharpe": "0", "pf": "0", "maxdd": "0", "winrate": "0",
        "cagr": "0", "sortino": "0",
    }


def load_csv_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def append_csv(path: Path, row: str):
    with open(path, "a", encoding="utf-8") as f:
        f.write(row + "\n")


def sf(val, default=0.0):
    try: return float(val)
    except: return default


def si(val, default=0):
    try: return int(float(val))
    except: return default


def sharpe_color(sharpe_str):
    s = sf(sharpe_str)
    if s > 0.5: return G
    if s > 0: return Y
    return R


# ── CSV init ───────────────────────────────────────────────────────────────
S1_HEADER = "strategy,group,name,trades,avg_profit_pct,tot_profit_usdt,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino,params"
S2_HEADER = "strategy,group,name,year,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino"
S3_HEADER = "strategy,group,name,window,phase,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,cagr,sortino"

for path, header in [(RESULTS_CSV, S1_HEADER), (YEARLY_CSV, S2_HEADER), (WF_CSV, S3_HEADER)]:
    if not path.exists():
        path.write_text(header + "\n", encoding="utf-8")

pipeline_start = time.time()

# ══════════════════════════════════════════════════════════════════════════
#  STAGE 1 — Full-sample screen
# ══════════════════════════════════════════════════════════════════════════
banner(f"STAGE 1 — Full-sample screen ({FULL_RANGE})")

done_s1 = {r["strategy"] for r in load_csv_rows(RESULTS_CSV)}
remaining = [e for e in manifest if e["strategy"] not in done_s1]
total = len(manifest)

cprint(Y, f"Resume: {len(done_s1)} strategies already done")
cprint(C, f"Manifest: {total} | Remaining: {len(remaining)}")

s1_completed = 0
s1_failed = 0
stage1_start = time.time()

for i, exp in enumerate(remaining):
    strategy = exp["strategy"]
    group = exp["group"]
    name = exp["name"]
    params_json = json.dumps(exp.get("params", {}), ensure_ascii=False)

    global_idx = len(done_s1) + i + 1
    pct = round(global_idx / total * 100, 1)
    elapsed = time.time() - stage1_start
    eta = round(elapsed / 60 / max(i, 1) * (len(remaining) - i)) if i > 0 else "?"

    cprint(C, f"[{global_idx}/{total}] ({pct}%) {group} :: {name}  ETA:~{eta}min")
    with open(PROGRESS_FILE, "a") as pf_file:
        pf_file.write(f"{time.strftime('%H:%M:%S')} [S1 {global_idx}/{total}] {strategy} - {name}\n")

    raw = run_backtest(strategy, FULL_RANGE)
    if not raw.strip():
        cprint(R, "  -> FAILED (empty output)")
        params_esc = params_json.replace('"', '""')
        append_csv(RESULTS_CSV, f'{strategy},{group},"{name}",FAILED,,,,,,,,,,"{params_esc}"')
        s1_failed += 1
        continue

    m = parse_backtest(raw)
    params_esc = params_json.replace('"', '""')
    append_csv(RESULTS_CSV,
        f'{strategy},{group},"{name}",{m["trades"]},{m["avg_profit"]},{m["tot_usdt"]},'
        f'{m["tot_pct"]},{m["sharpe"]},{m["pf"]},{m["maxdd"]},{m["winrate"]},'
        f'{m["cagr"]},{m["sortino"]},"{params_esc}"')

    cprint(sharpe_color(m["sharpe"]),
        f'  -> Trades={m["trades"]}  Sharpe={m["sharpe"]}  PF={m["pf"]}  '
        f'Profit={m["tot_pct"]}%  DD={m["maxdd"]}%')
    s1_completed += 1

    if sf(m["sharpe"]) >= 0.6:
        (RESULTS_DIR / f"v7_{strategy}_raw.txt").write_text(raw, encoding="utf-8")

cprint(G, f"\nSTAGE 1 DONE: total={total} completed={s1_completed} failed={s1_failed} resumed={len(done_s1)}")

# ══════════════════════════════════════════════════════════════════════════
#  STAGE 1.5 — Gate filter
# ══════════════════════════════════════════════════════════════════════════
all_results = load_csv_rows(RESULTS_CSV)
candidates = []
for r in all_results:
    if r.get("trades") == "FAILED":
        continue
    try:
        if (sf(r["sharpe"]) > S1["min_sharpe"] and
            sf(r["profit_factor"]) > S1["min_pf"] and
            si(r["trades"]) > S1["min_trades"] and
            sf(r["max_drawdown_pct"]) < S1["max_dd"]):
            candidates.append(r["strategy"])
    except:
        pass

banner(f"STAGE 1.5 — Gate filter: {len(candidates)} candidates pass")
results_by_strat = {r["strategy"]: r for r in all_results}
for c in candidates:
    r = results_by_strat.get(c, {})
    cprint(C, f'  * {c:<40} Sharpe={r.get("sharpe","?")}  PF={r.get("profit_factor","?")}  Trades={r.get("trades","?")}')

# ══════════════════════════════════════════════════════════════════════════
#  STAGE 2 — Yearly validation
# ══════════════════════════════════════════════════════════════════════════
yearly_periods = S2["yearly_periods"]
phase2_survivors = []

if not candidates:
    banner("STAGE 2 — SKIPPED (no S1 candidates)")
else:
    total_s2 = len(candidates) * len(yearly_periods)
    banner(f"STAGE 2 — Yearly validation ({len(candidates)} x {len(yearly_periods)} years = {total_s2} runs)")

    done_yearly = set()
    for r in load_csv_rows(YEARLY_CSV):
        done_yearly.add(f'{r["strategy"]}|{r.get("year","")}')
    cprint(Y, f"Resume: {len(done_yearly)} yearly rows already done")

    idx_s2 = 0
    stage2_start = time.time()

    for cand in candidates:
        r_info = results_by_strat.get(cand, {})
        group = r_info.get("group", "")
        name = r_info.get("name", "")

        for yp in yearly_periods:
            year = yp["year"]
            yrange = yp["range"]
            key = f"{cand}|{year}"
            idx_s2 += 1

            if key in done_yearly:
                continue

            pct = round(idx_s2 / total_s2 * 100)
            cprint(C, f"[{idx_s2}/{total_s2}] ({pct}%) {cand} / {year}")

            raw = run_backtest(cand, yrange)
            m = parse_backtest(raw)
            append_csv(YEARLY_CSV,
                f'{cand},{group},"{name}",{year},{yrange},{m["trades"]},'
                f'{m["tot_pct"]},{m["sharpe"]},{m["pf"]},{m["maxdd"]},'
                f'{m["winrate"]},{m["cagr"]},{m["sortino"]}')

            cprint(sharpe_color(m["sharpe"]),
                f'  -> Trades={m["trades"]}  Sharpe={m["sharpe"]}  PF={m["pf"]}  Profit={m["tot_pct"]}%')

    print(f"\n{Y}Evaluating yearly gates...{NC}")
    all_yearly = load_csv_rows(YEARLY_CSV)

    for cand in candidates:
        rows = [r for r in all_yearly if r["strategy"] == cand]
        eligible = [r for r in rows if si(r.get("trades")) >= 50]
        profitable = [r for r in eligible if sf(r.get("tot_profit_pct")) > 0]

        ok = True
        reason = "ok"
        if len(eligible) < 5:
            ok = False; reason = f"eligible years {len(eligible)} < 5"
        elif len(profitable) < 5:
            ok = False; reason = f"profitable years {len(profitable)} < 5"
        else:
            for yr in eligible:
                if sf(yr.get("sharpe")) < -0.5:
                    ok = False; reason = f'year {yr["year"]} Sharpe {yr["sharpe"]} < -0.5'; break
            bear = [r for r in rows if r.get("year") == "2022"]
            if ok and bear and si(bear[0].get("trades")) >= 50 and sf(bear[0].get("sharpe")) <= -0.3:
                ok = False; reason = f'2022 bear Sharpe {bear[0]["sharpe"]} <= -0.3'

        if ok:
            cprint(G, f"[PASS yearly] {cand}")
            phase2_survivors.append(cand)
        else:
            cprint(R, f"[FAIL yearly] {cand} :: {reason}")

    cprint(C, f"\nSTAGE 2 DONE: candidates={len(candidates)} pass={len(phase2_survivors)} fail={len(candidates)-len(phase2_survivors)}")

# ══════════════════════════════════════════════════════════════════════════
#  STAGE 3 — Walk-Forward
# ══════════════════════════════════════════════════════════════════════════
wf_windows = S3["walkforward_windows"]
s3_pass = 0

if not phase2_survivors:
    banner("STAGE 3 — SKIPPED (no S2 survivors)")
else:
    total_s3 = len(phase2_survivors) * len(wf_windows) * 2
    banner(f"STAGE 3 — Walk-Forward ({len(phase2_survivors)} survivors x {len(wf_windows)} windows = {total_s3} runs)")

    done_wf = set()
    for r in load_csv_rows(WF_CSV):
        done_wf.add(f'{r["strategy"]}|{r.get("window","")}|{r.get("phase","")}')

    idx_s3 = 0
    for surv in phase2_survivors:
        r_info = results_by_strat.get(surv, {})
        group = r_info.get("group", "")
        name = r_info.get("name", "")

        for w in wf_windows:
            win_name = w["name"]
            for phase in ["train", "test"]:
                idx_s3 += 1
                tr = w["train"] if phase == "train" else w["test"]
                key = f"{surv}|{win_name}|{phase}"
                if key in done_wf:
                    continue

                pct = round(idx_s3 / total_s3 * 100)
                cprint(C, f"[{idx_s3}/{total_s3}] ({pct}%) {surv} {win_name} {phase}")

                raw = run_backtest(surv, tr)
                m = parse_backtest(raw)
                append_csv(WF_CSV,
                    f'{surv},{group},"{name}",{win_name},{phase},{tr},{m["trades"]},'
                    f'{m["tot_pct"]},{m["sharpe"]},{m["pf"]},{m["maxdd"]},'
                    f'{m["cagr"]},{m["sortino"]}')

                color = G if sf(m["sharpe"]) > 0 else R
                cprint(color, f'  -> Sharpe={m["sharpe"]} PF={m["pf"]} Profit={m["tot_pct"]}%')

    print(f"\n{Y}Evaluating walk-forward gates...{NC}")
    all_wf = load_csv_rows(WF_CSV)

    for surv in phase2_survivors:
        ok = True
        reason = "ok"
        for w in wf_windows:
            test_rows = [r for r in all_wf if r["strategy"] == surv and r.get("window") == w["name"] and r.get("phase") == "test"]
            train_rows = [r for r in all_wf if r["strategy"] == surv and r.get("window") == w["name"] and r.get("phase") == "train"]
            if not test_rows or not train_rows:
                ok = False; reason = f'missing {w["name"]}'; break
            if sf(test_rows[0].get("sharpe")) <= 0:
                ok = False; reason = f'{w["name"]} test Sharpe <= 0'; break
            tpf = sf(test_rows[0].get("profit_factor"))
            trpf = sf(train_rows[0].get("profit_factor"))
            if trpf > 0 and tpf < trpf * 0.8:
                ok = False; reason = f'{w["name"]} PF decay'; break

        if ok:
            cprint(G, f"[PASS WF] {surv}")
            s3_pass += 1
        else:
            cprint(R, f"[FAIL WF] {surv} :: {reason}")

    cprint(C, f"STAGE 3 DONE: in={len(phase2_survivors)} pass={s3_pass} fail={len(phase2_survivors)-s3_pass}")

# ══════════════════════════════════════════════════════════════════════════
#  ANALYSIS
# ══════════════════════════════════════════════════════════════════════════
banner("ANALYSIS — Running analyze_v7.py")
analyze_script = WORK_DIR / "user_data" / "scripts" / "analyze_v7.py"
if analyze_script.exists():
    try:
        subprocess.run([sys.executable, str(analyze_script)], check=True)
        cprint(G, "Analysis complete. See experiment_results/v7_analysis.md")
    except subprocess.CalledProcessError:
        cprint(Y, "Analysis failed")
else:
    cprint(Y, "analyze_v7.py not found; skipping.")

# ══════════════════════════════════════════════════════════════════════════
#  SUMMARY
# ══════════════════════════════════════════════════════════════════════════
pipeline_end = time.time()
duration_s = int(pipeline_end - pipeline_start)
h, remainder = divmod(duration_s, 3600)
mins, secs = divmod(remainder, 60)

summary = f"""v7 Pipeline Summary
===================
Started:  {time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(pipeline_start))}
Ended:    {time.strftime('%m/%d/%Y %H:%M:%S', time.localtime(pipeline_end))}
Duration: {h:02d}:{mins:02d}:{secs:02d}

Stage 1:   completed={s1_completed} failed={s1_failed} resumed={len(done_s1)}
Stage 1.5: candidates={len(candidates)}
Stage 2:   pass={len(phase2_survivors)} fail={len(candidates)-len(phase2_survivors)}
Stage 3:   pass={s3_pass} fail={len(phase2_survivors)-s3_pass}
"""

SUMMARY_FILE.write_text(summary, encoding="utf-8")
cprint(M, summary)
cprint(G, "Pipeline complete!")
