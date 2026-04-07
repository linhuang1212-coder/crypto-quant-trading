#!/usr/bin/env bash
# One-click setup: Install Docker → Pull Freqtrade → Download data → Run V7 pipeline
# Usage: chmod +x setup_and_run_v7.sh && ./setup_and_run_v7.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}=== CryptoV11 量化实验环境设置 ===${NC}\n"

# ---------- Step 1: Check/Install Docker ----------
echo -e "${YELLOW}[1/4] 检查 Docker...${NC}"
if command -v docker &>/dev/null && docker info &>/dev/null 2>&1; then
    echo -e "${GREEN}Docker 已安装且运行中${NC}"
else
    if [ -d "/Applications/Docker.app" ]; then
        echo -e "${YELLOW}Docker Desktop 已安装但未运行，正在启动...${NC}"
        open -a Docker
        echo "等待 Docker 启动（最多60秒）..."
        for i in $(seq 1 60); do
            if docker info &>/dev/null 2>&1; then
                echo -e "${GREEN}Docker 已启动${NC}"
                break
            fi
            sleep 1
            printf "."
        done
        echo ""
        if ! docker info &>/dev/null 2>&1; then
            echo -e "${RED}Docker 启动超时，请手动启动 Docker Desktop 后重试${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Docker Desktop 未安装，正在通过 Homebrew 安装...${NC}"
        if ! command -v brew &>/dev/null; then
            echo -e "${RED}Homebrew 未安装。请先安装 Homebrew: https://brew.sh${NC}"
            exit 1
        fi
        brew install --cask docker
        echo -e "${YELLOW}请启动 Docker Desktop (从 Applications 打开)，然后重新运行此脚本${NC}"
        open -a Docker
        echo "等待 Docker 启动（最多90秒）..."
        for i in $(seq 1 90); do
            if docker info &>/dev/null 2>&1; then
                echo -e "${GREEN}Docker 已启动${NC}"
                break
            fi
            sleep 1
            printf "."
        done
        echo ""
        if ! docker info &>/dev/null 2>&1; then
            echo -e "${RED}Docker 启动超时，请手动启动后重新运行此脚本${NC}"
            exit 1
        fi
    fi
fi

# ---------- Step 2: Pull Freqtrade image ----------
echo -e "\n${YELLOW}[2/4] 拉取 Freqtrade Docker 镜像...${NC}"
docker pull freqtradeorg/freqtrade:stable
echo -e "${GREEN}Freqtrade 镜像就绪${NC}"

# ---------- Step 3: Download historical data ----------
echo -e "\n${YELLOW}[3/4] 下载历史数据 (BTC/ETH/SOL/ADA, 15m+4h, 2020-2026)...${NC}"

DATA_DIR="user_data/data/binance"
if [ -d "$DATA_DIR" ] && [ "$(ls -1 "$DATA_DIR"/*.json 2>/dev/null | wc -l)" -gt 4 ]; then
    echo -e "${GREEN}历史数据已存在 ($(ls -1 "$DATA_DIR"/*.json | wc -l) files)，跳过下载${NC}"
else
    echo "下载中...预计需要 5-10 分钟..."
    docker run --rm \
        -v "./user_data:/freqtrade/user_data" \
        freqtradeorg/freqtrade:stable download-data \
        --exchange binance \
        --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT ADA/USDT:USDT \
        --timeframes 15m 4h \
        --timerange 20200101-20260401 \
        --trading-mode futures \
        --config /freqtrade/user_data/config_backtest.json

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}历史数据下载完成${NC}"
    else
        echo -e "${RED}数据下载失败，请检查网络连接后重试${NC}"
        exit 1
    fi
fi

# ---------- Step 4: Run V7 experiments ----------
echo -e "\n${YELLOW}[4/4] 运行 V7 实验流水线 (154 策略 × 3 阶段)...${NC}"
echo -e "${CYAN}预估耗时: 10-18 小时（取决于 CPU 性能）${NC}"
echo ""

bash user_data/scripts/run_experiments_v7.sh

echo -e "\n${GREEN}=== 全部完成！查看结果: user_data/experiment_results/v7_analysis.md ===${NC}"
