#!/usr/bin/env bash
# V7 Experiment Pipeline: 3-stage anti-overfitting (full-sample → yearly → walk-forward) → analysis
# macOS/Linux compatible — all parsing via python3 (no grep -P)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$WORK_DIR"

DOCKER_IMAGE="freqtradeorg/freqtrade:stable"
STRATEGY_PATH_DOCKER="/freqtrade/user_data/strategies/experiments_v7"
DEFAULT_CONFIG_DOCKER="/freqtrade/user_data/config_backtest.json"

MANIFEST_PATH="user_data/experiment_manifest_v7.json"
GATES_PATH="user_data/configs/experiment_gates.json"
RESULTS_DIR="user_data/experiment_results"
RESULTS_CSV="$RESULTS_DIR/v7_results.csv"
YEARLY_CSV="$RESULTS_DIR/v7_yearly.csv"
WF_CSV="$RESULTS_DIR/v7_walkforward.csv"
PROGRESS_FILE="$RESULTS_DIR/v7_progress.txt"
SUMMARY_FILE="$RESULTS_DIR/v7_pipeline_summary.txt"

PIPELINE_START=$(date +%s)

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; MAGENTA='\033[0;35m'; NC='\033[0m'

banner() { echo -e "\n${MAGENTA}$(printf '=%.0s' {1..60})\n $1\n$(printf '=%.0s' {1..60})${NC}\n"; }

for f in "$MANIFEST_PATH" "$GATES_PATH"; do
    [ -f "$f" ] || { echo "FATAL: $f not found"; exit 1; }
done
mkdir -p "$RESULTS_DIR"

FULL_RANGE=$(python3 -c "import json; print(json.load(open('$GATES_PATH'))['full_sample_timerange'])")

run_backtest() {
    local strategy=$1 timerange=$2 spath=${3:-$STRATEGY_PATH_DOCKER}
    docker run --rm \
        -v "./user_data:/freqtrade/user_data" \
        "$DOCKER_IMAGE" backtesting \
        --config "$DEFAULT_CONFIG_DOCKER" \
        --strategy "$strategy" \
        --strategy-path "$spath" \
        --timerange "$timerange" \
        --cache none \
        --starting-balance 1000 2>&1
}

# Python-based parser — works on macOS and Linux, no grep -P needed
parse_backtest() {
    local output="$1"
    python3 -c "
import re, sys

text = sys.stdin.read()

def grab(pattern, default='0'):
    m = re.search(pattern, text)
    return m.group(1) if m else default

trades   = grab(r'Total/Daily Avg Trades.*?\s+(\d+)\s+/')
tot_pct  = grab(r'Total profit %.*?\s+([\-\d\.]+)%')
tot_usdt = grab(r'Absolute profit.*?\s+([\-\d\.]+)\s+USDT')
sharpe   = grab(r'Sharpe\s+.*?\s+([\-\d\.]+)\s*$', '0')
sortino  = grab(r'Sortino\s+.*?\s+([\-\d\.]+)\s*$', '0')
pf       = grab(r'Profit factor\s+.*?\s+([\-\d\.]+)\s*$', '0')
cagr     = grab(r'CAGR %\s+.*?\s+([\-\d\.]+)\s*$', '0')
maxdd    = grab(r'Absolute drawdown.*?\(([\d\.]+)%\)')
winrate  = grab(r'TOTAL\s+.*?\s+\d+\s+\d+\s+\d+\s+([\d\.]+)', '0')

avg_profit = '0'
try:
    t = int(trades)
    if t > 0:
        avg_profit = str(round(float(tot_pct) / t, 4))
except:
    pass

print(f'{trades}|{avg_profit}|{tot_usdt}|{tot_pct}|{sharpe}|{pf}|{maxdd}|{winrate}|{cagr}|{sortino}')
" <<< "$output"
}

# ========== Stage 1: Full-sample screen ==========
banner "STAGE 1 — Full-sample screen ($FULL_RANGE)"

TOTAL=$(python3 -c "import json; print(len(json.load(open('$MANIFEST_PATH'))))")
S1_COMPLETED=0; S1_FAILED=0; S1_RESUMED=0

declare -A DONE_S1
if [ -f "$RESULTS_CSV" ]; then
    while IFS= read -r line; do
        strat=$(echo "$line" | cut -d',' -f1)
        [ -n "$strat" ] && DONE_S1["$strat"]=1
    done < <(tail -n +2 "$RESULTS_CSV")
    S1_RESUMED=${#DONE_S1[@]}
    echo -e "${YELLOW}Resume: $S1_RESUMED strategies already in v7_results.csv${NC}"
else
    echo "strategy,group,name,trades,avg_profit_pct,tot_profit_usdt,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino,params" > "$RESULTS_CSV"
fi

REMAINING_JSON=$(python3 -c "
import json
manifest = json.load(open('$MANIFEST_PATH'))
done = set(line.split(',')[0] for line in open('$RESULTS_CSV').read().strip().split('\n')[1:] if line.strip())
remaining = [e for e in manifest if e['strategy'] not in done]
print(json.dumps(remaining))
")
REMAINING_COUNT=$(echo "$REMAINING_JSON" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
echo -e "${CYAN}Manifest: $TOTAL | Remaining: $REMAINING_COUNT${NC}"

STAGE1_START=$(date +%s)

for i in $(seq 0 $((REMAINING_COUNT - 1))); do
    EXP=$(echo "$REMAINING_JSON" | python3 -c "
import json,sys
data = json.load(sys.stdin)[$i]
params_json = json.dumps(data.get('params', {}), ensure_ascii=False)
print(f\"{data['strategy']}|{data['group']}|{data['name']}|{params_json}\")
")
    IFS='|' read -r STRATEGY GROUP NAME PARAMS_JSON <<< "$EXP"

    GLOBAL_IDX=$((S1_RESUMED + i + 1))
    PCT=$(python3 -c "print(round($GLOBAL_IDX / $TOTAL * 100, 1))")
    ELAPSED=$(($(date +%s) - STAGE1_START))
    if [ "$i" -gt 0 ]; then
        ETA_MIN=$(python3 -c "print(round($ELAPSED / 60 / $i * ($REMAINING_COUNT - $i), 0))")
    else
        ETA_MIN="?"
    fi

    echo -e "${CYAN}[$GLOBAL_IDX/$TOTAL] ($PCT%) $GROUP :: $NAME  ETA:~${ETA_MIN}min${NC}"
    echo "$(date '+%H:%M:%S') [S1 $GLOBAL_IDX/$TOTAL] $STRATEGY - $NAME" >> "$PROGRESS_FILE"

    RAW=$(run_backtest "$STRATEGY" "$FULL_RANGE" || true)
    if [ -z "$RAW" ]; then
        echo -e "${RED}  -> FAILED (empty output)${NC}"
        PARAMS_ESC=$(echo "$PARAMS_JSON" | sed 's/"/""/g')
        echo "$STRATEGY,$GROUP,\"$NAME\",FAILED,,,,,,,,,,\"$PARAMS_ESC\"" >> "$RESULTS_CSV"
        S1_FAILED=$((S1_FAILED + 1))
        continue
    fi

    PARSED=$(parse_backtest "$RAW")
    IFS='|' read -r TRADES AVG_PROFIT TOT_USDT TOT_PCT SHARPE PF MAXDD WINRATE CAGR SORTINO <<< "$PARSED"
    PARAMS_ESC=$(echo "$PARAMS_JSON" | sed 's/"/""/g')
    echo "$STRATEGY,$GROUP,\"$NAME\",$TRADES,$AVG_PROFIT,$TOT_USDT,$TOT_PCT,$SHARPE,$PF,$MAXDD,$WINRATE,$CAGR,$SORTINO,\"$PARAMS_ESC\"" >> "$RESULTS_CSV"

    COLOR=$RED
    SH_CMP=$(python3 -c "print(1 if float('$SHARPE') > 0.5 else 0)" 2>/dev/null || echo 0)
    SH_CMP2=$(python3 -c "print(1 if float('$SHARPE') > 0 else 0)" 2>/dev/null || echo 0)
    [ "$SH_CMP" = "1" ] && COLOR=$GREEN
    [ "$SH_CMP" = "0" ] && [ "$SH_CMP2" = "1" ] && COLOR=$YELLOW
    echo -e "${COLOR}  -> Trades=$TRADES  Sharpe=$SHARPE  PF=$PF  Profit=${TOT_PCT}%  DD=${MAXDD}%${NC}"
    S1_COMPLETED=$((S1_COMPLETED + 1))

    SH_SAVE=$(python3 -c "print(1 if float('$SHARPE') >= 0.6 else 0)" 2>/dev/null || echo 0)
    if [ "$SH_SAVE" = "1" ]; then
        echo "$RAW" > "$RESULTS_DIR/v7_${STRATEGY}_raw.txt"
    fi
done

echo -e "\n${GREEN}STAGE 1 DONE: total=$TOTAL completed=$S1_COMPLETED failed=$S1_FAILED resumed=$S1_RESUMED${NC}"

# ========== Stage 1.5: Gate filter ==========
S1_CANDIDATES=$(python3 -c "
import json, csv
gates = json.load(open('$GATES_PATH'))
min_sh = gates['stage1']['min_sharpe']
min_pf = gates['stage1']['min_pf']
min_tr = gates['stage1']['min_trades']
max_dd = gates['stage1']['max_dd']
candidates = []
with open('$RESULTS_CSV', newline='', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        if r.get('trades','') == 'FAILED': continue
        try:
            if float(r['sharpe']) > min_sh and float(r['profit_factor']) > min_pf and int(r['trades']) > min_tr and float(r['max_drawdown_pct']) < max_dd:
                candidates.append(r['strategy'])
        except: pass
print(json.dumps(candidates))
")
S1_CAND_COUNT=$(echo "$S1_CANDIDATES" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")

banner "STAGE 1.5 — Gate filter: $S1_CAND_COUNT candidates pass"
echo "$S1_CANDIDATES" | python3 -c "
import json, sys, csv
cands = json.load(sys.stdin)
if not cands:
    print('  No candidates passed Stage 1 gate.')
else:
    with open('$RESULTS_CSV', newline='', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            if r['strategy'] in cands:
                print(f\"  * {r['strategy']:<40} Sharpe={r['sharpe']}  PF={r['profit_factor']}  Trades={r['trades']}\")
"

# ========== Stage 2: Yearly validation ==========
S2_PASS=0; S2_FAIL=0; S2_SURVIVORS="[]"
if [ "$S1_CAND_COUNT" -eq 0 ]; then
    banner "STAGE 2 — SKIPPED (no S1 candidates)"
else
    YEARLY_PERIODS=$(python3 -c "import json; print(json.dumps(json.load(open('$GATES_PATH'))['stage2']['yearly_periods']))")
    N_YEARS=$(echo "$YEARLY_PERIODS" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
    TOTAL_S2=$((S1_CAND_COUNT * N_YEARS))

    banner "STAGE 2 — Yearly validation ($S1_CAND_COUNT x $N_YEARS years = $TOTAL_S2 runs)"

    if [ ! -f "$YEARLY_CSV" ]; then
        echo "strategy,group,name,year,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,win_rate,cagr,sortino" > "$YEARLY_CSV"
    fi

    declare -A DONE_Y
    if [ -f "$YEARLY_CSV" ]; then
        while IFS= read -r line; do
            strat=$(echo "$line" | cut -d',' -f1)
            year=$(echo "$line" | cut -d',' -f4)
            [ -n "$strat" ] && DONE_Y["${strat}|${year}"]=1
        done < <(tail -n +2 "$YEARLY_CSV")
        echo -e "${YELLOW}Resume: ${#DONE_Y[@]} yearly rows already done${NC}"
    fi

    STAGE2_START=$(date +%s)
    IDX_S2=0

    for cand_idx in $(seq 0 $((S1_CAND_COUNT - 1))); do
        STRATEGY=$(echo "$S1_CANDIDATES" | python3 -c "import json,sys; print(json.load(sys.stdin)[$cand_idx])")
        ROW_INFO=$(python3 -c "
import csv
with open('$RESULTS_CSV', newline='', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        if r['strategy'] == '$STRATEGY':
            print(r['group'] + '|' + r['name'])
            break
")
        IFS='|' read -r GROUP NAME <<< "$ROW_INFO"

        for yr_idx in $(seq 0 $((N_YEARS - 1))); do
            YR_DATA=$(echo "$YEARLY_PERIODS" | python3 -c "import json,sys; d=json.load(sys.stdin)[$yr_idx]; print(d['year'] + '|' + d['range'])")
            IFS='|' read -r YEAR RANGE <<< "$YR_DATA"
            KEY="${STRATEGY}|${YEAR}"
            IDX_S2=$((IDX_S2 + 1))

            if [ -n "${DONE_Y[$KEY]+x}" ]; then continue; fi

            PCT=$((IDX_S2 * 100 / TOTAL_S2))
            echo -e "${CYAN}[$IDX_S2/$TOTAL_S2] ($PCT%) $STRATEGY / $YEAR${NC}"

            RAW=$(run_backtest "$STRATEGY" "$RANGE" || true)
            PARSED=$(parse_backtest "$RAW")
            IFS='|' read -r TRADES AVG_PROFIT TOT_USDT TOT_PCT SHARPE PF MAXDD WINRATE CAGR SORTINO <<< "$PARSED"
            echo "$STRATEGY,$GROUP,\"$NAME\",$YEAR,$RANGE,$TRADES,$TOT_PCT,$SHARPE,$PF,$MAXDD,$WINRATE,$CAGR,$SORTINO" >> "$YEARLY_CSV"

            COLOR=$RED
            SH_CMP=$(python3 -c "print(1 if float('$SHARPE') > 0.3 else 0)" 2>/dev/null || echo 0)
            SH_CMP2=$(python3 -c "print(1 if float('$SHARPE') >= 0 else 0)" 2>/dev/null || echo 0)
            [ "$SH_CMP" = "1" ] && COLOR=$GREEN
            [ "$SH_CMP" = "0" ] && [ "$SH_CMP2" = "1" ] && COLOR=$YELLOW
            echo -e "${COLOR}  -> Trades=$TRADES  Sharpe=$SHARPE  PF=$PF  Profit=${TOT_PCT}%${NC}"
        done
    done

    echo -e "\n${YELLOW}Evaluating yearly gates...${NC}"
    S2_SURVIVORS=$(python3 -c "
import json, csv
gates = json.load(open('$GATES_PATH'))
candidates = json.loads('$(echo "$S1_CANDIDATES")')
yearly = list(csv.DictReader(open('$YEARLY_CSV', newline='', encoding='utf-8-sig')))
survivors = []
for s in candidates:
    rows = [r for r in yearly if r['strategy'] == s]
    eligible = [r for r in rows if int(r.get('trades','0')) >= 50]
    profitable = [r for r in eligible if float(r.get('tot_profit_pct','0')) > 0]
    if len(eligible) < 5:
        print(f'[FAIL yearly] {s} :: eligible years {len(eligible)} < 5')
        continue
    if len(profitable) < 5:
        print(f'[FAIL yearly] {s} :: profitable years {len(profitable)} < 5')
        continue
    bad = False
    for r in eligible:
        if float(r.get('sharpe','0')) < -0.5:
            print(f'[FAIL yearly] {s} :: year {r[\"year\"]} Sharpe {r[\"sharpe\"]} < -0.5')
            bad = True; break
    bear = [r for r in rows if r.get('year','') == '2022']
    if not bad and bear and int(bear[0].get('trades','0')) >= 50 and float(bear[0].get('sharpe','0')) <= -0.3:
        print(f'[FAIL yearly] {s} :: 2022 bear Sharpe {bear[0][\"sharpe\"]} <= -0.3')
        bad = True
    if not bad:
        print(f'[PASS yearly] {s}')
        survivors.append(s)
print('---JSON---')
print(json.dumps(survivors))
")
    S2_SURVIVORS=$(echo "$S2_SURVIVORS" | sed -n '/---JSON---/{n;p;}')
    S2_PASS=$(echo "$S2_SURVIVORS" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
    S2_FAIL=$((S1_CAND_COUNT - S2_PASS))
    echo -e "\n${CYAN}STAGE 2 DONE: candidates=$S1_CAND_COUNT pass=$S2_PASS fail=$S2_FAIL${NC}"
fi

# ========== Stage 3: Walk-Forward ==========
S2_SURV_COUNT=$(echo "$S2_SURVIVORS" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo 0)
S3_PASS=0; S3_FAIL=0
if [ "$S2_SURV_COUNT" -eq 0 ]; then
    banner "STAGE 3 — SKIPPED (no S2 survivors)"
else
    WF_WINDOWS=$(python3 -c "import json; print(json.dumps(json.load(open('$GATES_PATH'))['stage3']['walkforward_windows']))")
    N_WIN=$(echo "$WF_WINDOWS" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
    TOTAL_S3=$((S2_SURV_COUNT * N_WIN * 2))

    banner "STAGE 3 — Walk-Forward ($S2_SURV_COUNT survivors x $N_WIN windows = $TOTAL_S3 runs)"

    if [ ! -f "$WF_CSV" ]; then
        echo "strategy,group,name,window,phase,timerange,trades,tot_profit_pct,sharpe,profit_factor,max_drawdown_pct,cagr,sortino" > "$WF_CSV"
    fi

    declare -A DONE_WF
    if [ -f "$WF_CSV" ]; then
        while IFS= read -r line; do
            strat=$(echo "$line" | cut -d',' -f1)
            win=$(echo "$line" | cut -d',' -f4)
            phase=$(echo "$line" | cut -d',' -f5)
            [ -n "$strat" ] && DONE_WF["${strat}|${win}|${phase}"]=1
        done < <(tail -n +2 "$WF_CSV")
    fi

    STAGE3_START=$(date +%s)
    IDX_S3=0

    for surv_idx in $(seq 0 $((S2_SURV_COUNT - 1))); do
        STRATEGY=$(echo "$S2_SURVIVORS" | python3 -c "import json,sys; print(json.load(sys.stdin)[$surv_idx])")
        ROW_INFO=$(python3 -c "
import csv
with open('$RESULTS_CSV', newline='', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        if r['strategy'] == '$STRATEGY':
            print(r['group'] + '|' + r['name'])
            break
")
        IFS='|' read -r GROUP NAME <<< "$ROW_INFO"

        for win_idx in $(seq 0 $((N_WIN - 1))); do
            WIN_DATA=$(echo "$WF_WINDOWS" | python3 -c "import json,sys; d=json.load(sys.stdin)[$win_idx]; print(d['name'] + '|' + d['train'] + '|' + d['test'])")
            IFS='|' read -r WIN_NAME TRAIN_RANGE TEST_RANGE <<< "$WIN_DATA"

            for PHASE in train test; do
                IDX_S3=$((IDX_S3 + 1))
                if [ "$PHASE" = "train" ]; then TR="$TRAIN_RANGE"; else TR="$TEST_RANGE"; fi
                KEY="${STRATEGY}|${WIN_NAME}|${PHASE}"
                if [ -n "${DONE_WF[$KEY]+x}" ]; then continue; fi

                PCT=$((IDX_S3 * 100 / TOTAL_S3))
                echo -e "${CYAN}[$IDX_S3/$TOTAL_S3] ($PCT%) $STRATEGY $WIN_NAME $PHASE${NC}"

                RAW=$(run_backtest "$STRATEGY" "$TR" || true)
                PARSED=$(parse_backtest "$RAW")
                IFS='|' read -r TRADES AVG_PROFIT TOT_USDT TOT_PCT SHARPE PF MAXDD WINRATE CAGR SORTINO <<< "$PARSED"
                echo "$STRATEGY,$GROUP,\"$NAME\",$WIN_NAME,$PHASE,$TR,$TRADES,$TOT_PCT,$SHARPE,$PF,$MAXDD,$CAGR,$SORTINO" >> "$WF_CSV"

                COLOR=$RED
                SH_POS=$(python3 -c "print(1 if float('$SHARPE') > 0 else 0)" 2>/dev/null || echo 0)
                [ "$SH_POS" = "1" ] && COLOR=$GREEN
                echo -e "${COLOR}  -> Sharpe=$SHARPE PF=$PF Profit=${TOT_PCT}%${NC}"
            done
        done
    done

    echo -e "\n${YELLOW}Evaluating walk-forward gates...${NC}"
    S3_RESULT=$(python3 -c "
import json, csv
survivors = json.loads('$(echo "$S2_SURVIVORS")')
wf_windows = json.load(open('$GATES_PATH'))['stage3']['walkforward_windows']
wf = list(csv.DictReader(open('$WF_CSV', newline='', encoding='utf-8-sig')))
passed = 0
for s in survivors:
    ok = True
    reason = 'ok'
    for w in wf_windows:
        test_rows = [r for r in wf if r['strategy']==s and r['window']==w['name'] and r['phase']=='test']
        train_rows = [r for r in wf if r['strategy']==s and r['window']==w['name'] and r['phase']=='train']
        if not test_rows or not train_rows:
            ok=False; reason=f'missing {w[\"name\"]}'; break
        if float(test_rows[0].get('sharpe','0')) <= 0:
            ok=False; reason=f'{w[\"name\"]} test Sharpe <= 0'; break
        tpf = float(test_rows[0].get('profit_factor','0'))
        trpf = float(train_rows[0].get('profit_factor','0'))
        if trpf > 0 and tpf < trpf * 0.8:
            ok=False; reason=f'{w[\"name\"]} PF decay'; break
    if ok:
        print(f'[PASS WF] {s}')
        passed += 1
    else:
        print(f'[FAIL WF] {s} :: {reason}')
print(f'---PASS_COUNT={passed}---')
")
    echo "$S3_RESULT" | grep -v '^---'
    S3_PASS=$(echo "$S3_RESULT" | grep -o 'PASS_COUNT=[0-9]*' | cut -d= -f2)
    S3_FAIL=$((S2_SURV_COUNT - S3_PASS))
    echo -e "${CYAN}STAGE 3 DONE: in=$S2_SURV_COUNT pass=$S3_PASS fail=$S3_FAIL${NC}"
fi

# ========== Analysis ==========
banner "ANALYSIS — Running analyze_v7.py"
ANALYZE_SCRIPT="user_data/scripts/analyze_v7.py"
if [ -f "$ANALYZE_SCRIPT" ]; then
    python3 "$ANALYZE_SCRIPT" && echo -e "${GREEN}Analysis complete. See experiment_results/v7_analysis.md${NC}" || echo -e "${YELLOW}Analysis failed${NC}"
else
    echo -e "${YELLOW}analyze_v7.py not found; skipping.${NC}"
fi

# ========== Summary ==========
PIPELINE_END=$(date +%s)
DURATION=$(python3 -c "
s=$PIPELINE_END - $PIPELINE_START
h=int(s//3600); m=int((s%3600)//60); sec=int(s%60)
print(f'{h:02d}:{m:02d}:{sec:02d}')
")

SUMMARY="v7 Pipeline Summary
===================
Started:  $(date -r $PIPELINE_START '+%m/%d/%Y %H:%M:%S' 2>/dev/null || date '+%m/%d/%Y %H:%M:%S')
Ended:    $(date -r $PIPELINE_END '+%m/%d/%Y %H:%M:%S' 2>/dev/null || date '+%m/%d/%Y %H:%M:%S')
Duration: $DURATION

Stage 1:   completed=$S1_COMPLETED failed=$S1_FAILED resumed=$S1_RESUMED
Stage 1.5: candidates=${S1_CAND_COUNT:-0}
Stage 2:   pass=${S2_PASS:-0} fail=${S2_FAIL:-0}
Stage 3:   pass=${S3_PASS:-0} fail=${S3_FAIL:-0}
"

echo "$SUMMARY" > "$SUMMARY_FILE"
echo -e "${MAGENTA}$SUMMARY${NC}"
echo -e "${GREEN}Pipeline complete!${NC}"
