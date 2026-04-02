# 加密货币量化交易系统 CryptoV10

基于 Freqtrade + Docker 的加密货币自动化交易系统。采用 Donchian 通道趋势突破策略，配合多层风控体系和因子监控，追求稳健盈利。

## 策略概览

**CryptoV10** — 15m Donchian 趋势突破 Long-Only

| 参数 | 值 |
|------|-----|
| 交易品种 | BTC/USDT, ETH/USDT, SOL/USDT, ADA/USDT |
| 时间框架 | 15m（主） + 4H（多时间框架确认） |
| 入场方式 | Donchian 20 突破 + 11 个过滤条件 |
| 止损 | -10% 硬止损 |
| 止盈 | Trailing Stop（利润 30% 后激活，10% 追踪距离） |
| 杠杆 | 5x isolated |
| 仓位管理 | 复利模式，40% tradable_balance_ratio |

### 入场条件（全部满足才开仓）

1. 价格突破 Donchian 20 上轨
2. ATR 突破强度过滤：`(close - dc_upper) > atr * 0.5`
3. ADX > 28 且 ADX 上升
4. +DI > -DI，DI 差值 > 5
5. EMA21 > EMA55 > EMA200（多头排列）
6. EMA200 斜率 > 0
7. 4H EMA21 > 4H EMA55（多时间框架确认）
8. OBV > OBV_EMA（成交量确认）

### 风控体系

| 层级 | 机制 | 说明 |
|------|------|------|
| 单笔 | 硬止损 -10% | 防止单笔巨亏 |
| 单笔 | Trailing Stop | 利润跑到 30% 后激活追踪 |
| 单笔 | 超时平仓 | 64 bars 亏损退出 / 128 bars 强制退出 |
| 单笔 | 大止盈 | 利润 >= 40% 立即平仓 |
| 日内 | 冷却期 | 止损后 24 bars（6小时）不入场 |
| 日内 | 最大亏损 | 当日止损达 4 笔后暂停交易 |
| 总体 | 最大持仓 | 4 笔（每个品种最多 1 笔） |

## 回测表现

**全样本 2020-2026，$1,300 本金，40% 复利：**

| 指标 | 值 |
|------|-----|
| 最终余额 | $6,841 |
| 总利润 | +$5,541（+426%） |
| CAGR | 30.5% |
| Sharpe | 0.77 |
| Sortino | 2.68 |
| Profit Factor | 1.23 |
| 最大回撤 | 16.3% |
| 交易数 | 1,179 笔 |
| 胜率 | 33.4% |

### 分年度表现

| 年度 | 利润% | Sharpe | PF | 最大回撤 |
|------|--------|--------|-----|---------|
| 2020 | +74.7% | 1.29 | 1.33 | 16.9% |
| 2021 | +42.3% | 0.81 | 1.14 | 22.6% |
| 2022 | -15.2% | -0.50 | 0.83 | 23.2% |
| 2023 | +51.4% | 0.85 | 1.21 | 28.2% |
| 2024 | +42.1% | 1.06 | 1.33 | 14.0% |
| 2025-Q1 | +28.5% | 0.57 | 1.19 | 21.1% |

6 年中 5 年盈利，仅 2022 熊市小亏。

## 项目结构

```
freqtrade/
├── user_data/
│   ├── strategies/
│   │   ├── CryptoV10.py          # 核心策略
│   │   └── MarketStateBot.py     # 市场状态机器人
│   ├── scripts/
│   │   ├── ic_monitor.py         # IC 因子监控脚本
│   │   └── download_fng.py       # Fear & Greed 数据下载
│   ├── config.json.example       # 配置示例（需复制为 config.json 并填入 API 密钥）
│   └── trading_journal.md        # 交易日志
├── .cursor/rules/
│   └── crypto-quant-trader.mdc   # AI 辅助规则
└── .gitignore
```

## 快速开始

### 1. 环境准备

需要安装 [Docker](https://www.docker.com/)。

```bash
git clone https://github.com/linhuang1212-coder/crypto-quant-trading.git
cd crypto-quant-trading
```

### 2. 配置

```bash
cp user_data/config.json.example user_data/config.json
```

编辑 `user_data/config.json`，填入：
- Binance API Key 和 Secret
- Telegram Bot Token 和 Chat ID（可选）

### 3. 下载历史数据

```bash
docker run --rm -v "./user_data:/freqtrade/user_data" \
  freqtradeorg/freqtrade:stable download-data \
  --exchange binance \
  --pairs BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT ADA/USDT:USDT \
  --timeframes 15m 4h \
  --timerange 20200101-20260401 \
  --trading-mode futures
```

### 4. 回测

```bash
docker run --rm -v "./user_data:/freqtrade/user_data" \
  freqtradeorg/freqtrade:stable backtesting \
  --config /freqtrade/user_data/config.json \
  --strategy CryptoV10 \
  --timerange 20200101-20260401 \
  --cache none \
  --starting-balance 1300
```

### 5. 实盘运行

```bash
docker run -d --name freqtrade --restart unless-stopped \
  -v "./user_data:/freqtrade/user_data" \
  -p 8080:8080 \
  freqtradeorg/freqtrade:stable trade \
  --config /freqtrade/user_data/config.json \
  --strategy CryptoV10
```

## 监控工具

### IC 因子监控

积累 30+ 笔实盘交易后，运行因子有效性分析：

```bash
docker run --rm -v "./user_data:/freqtrade/user_data" \
  freqtradeorg/freqtrade:stable \
  python /freqtrade/user_data/scripts/ic_monitor.py
```

### 日常监控

- **Telegram**：自动推送开仓/平仓通知
- **Web UI**：`http://localhost:8080`
- **日志**：`docker logs freqtrade --tail 20`

## 已验证的经验

- Trailing Stop 的 offset 值对趋势策略至关重要：越高 → 盈亏比越好
- Long-Only 策略长期表现优于双向策略
- ATR 突破强度过滤可有效减少假突破，大幅降低回撤
- 止损后冷却期（6 小时）可减少连续止损，提升 Sharpe
- Fear & Greed 指数不适合作为入场过滤（经回测验证，加入后利润和 Sharpe 均下降）
- 品种筛选至关重要：DOGE/LINK/XRP/AVAX/BNB 在此策略下表现为负

## 免责声明

本项目仅供学习研究，不构成投资建议。量化交易有风险，过去的回测表现不代表未来收益。
