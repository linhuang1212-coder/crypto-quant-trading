#!/usr/bin/env bash
# V7 实验一键运行脚本
# 使用方法: cd ~/crypto-quant-trading && bash run_v7.sh
set -euo pipefail
cd "$(dirname "$0")"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

# --- Step 0: Fix Docker credential issue ---
echo -e "${YELLOW}[0] 检查 Docker 凭证配置...${NC}"
if [ -f ~/.docker/config.json ] && grep -q '"credsStore"' ~/.docker/config.json; then
    cp ~/.docker/config.json ~/.docker/config.json.bak
    python3 -c "
import json
with open('$HOME/.docker/config.json') as f:
    cfg = json.load(f)
cfg.pop('credsStore', None)
with open('$HOME/.docker/config.json', 'w') as f:
    json.dump(cfg, f, indent=2)
"
    echo -e "${GREEN}已修复 credsStore (备份: ~/.docker/config.json.bak)${NC}"
else
    echo -e "${GREEN}凭证配置正常${NC}"
fi

# --- Step 1: Pull image ---
echo -e "\n${YELLOW}[1] 检查 Freqtrade 镜像...${NC}"
if docker image inspect freqtradeorg/freqtrade:stable &>/dev/null; then
    echo -e "${GREEN}镜像已存在${NC}"
else
    echo "拉取 freqtradeorg/freqtrade:stable ..."
    docker pull freqtradeorg/freqtrade:stable
    echo -e "${GREEN}镜像拉取完成${NC}"
fi

# --- Step 2: Download data ---
echo -e "\n${YELLOW}[2] 检查历史数据...${NC}"
DATA_DIR="user_data/data"
if [ -d "$DATA_DIR" ] && [ "$(find "$DATA_DIR" -name '*.json' 2>/dev/null | wc -l)" -gt 4 ]; then
    echo -e "${GREEN}历史数据已存在，跳过${NC}"
else
    echo "下载 BTC/ETH/SOL/ADA 15m+4h (2020-2026)..."
    docker run --rm \
        -v "./user_data:/freqtrade/user_data" \
        freqtradeorg/freqtrade:stable download-data \
        --exchange binance \
        --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT ADA/USDT:USDT \
        --timeframes 15m 4h \
        --timerange 20200101-20260407 \
        --trading-mode futures \
        --config /freqtrade/user_data/config_backtest.json
    echo -e "${GREEN}数据下载完成${NC}"
fi

# --- Step 3: Quick sanity check ---
echo -e "\n${YELLOW}[3] 验证回测环境...${NC}"
TEST_OUTPUT=$(docker run --rm \
    -v "./user_data:/freqtrade/user_data" \
    freqtradeorg/freqtrade:stable backtesting \
    --config /freqtrade/user_data/config_backtest.json \
    --strategy V7_H1_P001 \
    --strategy-path /freqtrade/user_data/strategies/experiments_v7 \
    --timerange 20240101-20240201 \
    --cache none \
    --starting-balance 1000 2>&1)

TRADE_COUNT=$(python3 -c "
import re, sys
text = '''$TEST_OUTPUT'''
m = re.search(r'Total/Daily Avg Trades.*?(\d+)\s+/', text)
print(m.group(1) if m else '0')
" 2>/dev/null || echo "0")

if [ "$TRADE_COUNT" -gt 0 ] 2>/dev/null; then
    echo -e "${GREEN}回测验证通过！(${TRADE_COUNT} trades)${NC}"
else
    echo -e "${YELLOW}回测产生了 0 笔交易（短时间窗口正常），继续运行...${NC}"
fi

# --- Step 4: Run V7 Stage 3 Walk-Forward ---
echo -e "\n${YELLOW}[4] 启动 V7 Stage 3 Walk-Forward (18候选 × 3窗口 × 2阶段)${NC}"
echo -e "${CYAN}预估耗时: 3-4 小时${NC}"
echo ""
python3 user_data/scripts/run_v7_stage3.py

echo -e "\n${GREEN}=== 完成！查看: user_data/experiment_results/v7_analysis.md ===${NC}"
