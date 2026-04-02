"""
IC Factor Monitor - 因子 Information Coefficient 监控
====================================================
用法: python ic_monitor.py [--min-trades 30]

读取 factor_snapshots.json 和 Freqtrade 交易数据库，
计算各因子与交易盈亏的 IC（Rank Correlation），检测因子衰减。

IC 评估标准:
  优秀: |IC| >= 0.10 且 |IC_IR| >= 0.5
  良好: |IC| >= 0.05 且 |IC_IR| >= 0.3
  无效: |IC| < 0.03 → 考虑淘汰
"""

import json
import sys
import os
import sqlite3
from datetime import datetime

import numpy as np


SNAPSHOT_PATH = "/freqtrade/user_data/factor_snapshots.json"
DB_PATH = "/freqtrade/user_data/tradesv3.sqlite"

FACTORS = ['adx', 'plus_di', 'minus_di', 'di_diff', 'atr', 'ema200_slope', 'obv_ratio']


def load_snapshots(path: str) -> list:
    if not os.path.exists(path):
        print(f"[ERROR] 快照文件不存在: {path}")
        return []
    with open(path) as f:
        return json.load(f)


def load_trades(db_path: str) -> dict:
    if not os.path.exists(db_path):
        print(f"[ERROR] 数据库不存在: {db_path}")
        return {}
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT pair, open_date, close_profit
        FROM trades
        WHERE is_open = 0 AND close_profit IS NOT NULL
        ORDER BY open_date
    """)
    trades = {}
    for row in cur.fetchall():
        key = f"{row['pair']}_{row['open_date']}"
        trades[key] = row['close_profit']
    conn.close()
    return trades


def match_snapshots_to_trades(snapshots: list, trades: dict) -> list:
    """Match factor snapshots to trade outcomes by pair + approximate time."""
    matched = []
    for snap in snapshots:
        snap_time = snap['time'][:19]
        pair = snap['pair']
        best_match = None
        best_diff = float('inf')
        for key, profit in trades.items():
            if not key.startswith(pair):
                continue
            trade_time = key.split('_', 1)[1][:19]
            try:
                t1 = datetime.fromisoformat(snap_time)
                t2 = datetime.fromisoformat(trade_time)
                diff = abs((t1 - t2).total_seconds())
                if diff < best_diff and diff < 300:
                    best_diff = diff
                    best_match = profit
            except (ValueError, TypeError):
                continue
        if best_match is not None:
            matched.append({**snap, 'profit': best_match})
    return matched


def calc_rank_ic(values: list, profits: list) -> float:
    """Spearman rank correlation (IC)."""
    n = len(values)
    if n < 5:
        return 0.0
    rank_v = np.argsort(np.argsort(values)).astype(float)
    rank_p = np.argsort(np.argsort(profits)).astype(float)
    d = rank_v - rank_p
    return 1 - (6 * np.sum(d ** 2)) / (n * (n ** 2 - 1))


def analyze_ic(matched: list, min_trades: int = 30):
    if len(matched) < min_trades:
        print(f"\n[INFO] 交易数据不足: {len(matched)} 笔 (需要 >= {min_trades})")
        print("       继续积累实盘交易后再运行此脚本。")
        return

    profits = [m['profit'] for m in matched]

    print(f"\n{'='*60}")
    print(f"  IC 因子监控报告 — {len(matched)} 笔交易")
    print(f"{'='*60}\n")
    print(f"{'因子':<16} {'IC':>8} {'|IC|':>8} {'评级':>8}")
    print(f"{'-'*16} {'-'*8} {'-'*8} {'-'*8}")

    for factor in FACTORS:
        values = [m.get(factor, 0) for m in matched]
        if all(v == values[0] for v in values):
            print(f"{factor:<16} {'N/A':>8} {'N/A':>8} {'无变化':>8}")
            continue
        ic = calc_rank_ic(values, profits)
        abs_ic = abs(ic)
        if abs_ic >= 0.10:
            grade = "优秀"
        elif abs_ic >= 0.05:
            grade = "良好"
        elif abs_ic >= 0.03:
            grade = "一般"
        else:
            grade = "无效"
        print(f"{factor:<16} {ic:>8.4f} {abs_ic:>8.4f} {grade:>8}")

    print(f"\n{'='*60}")
    print("评级标准: 优秀 |IC|>=0.10 | 良好 |IC|>=0.05 | 一般 |IC|>=0.03 | 无效 <0.03")
    print("无效因子应考虑淘汰或替换。")


def main():
    min_trades = 30
    if '--min-trades' in sys.argv:
        idx = sys.argv.index('--min-trades')
        if idx + 1 < len(sys.argv):
            min_trades = int(sys.argv[idx + 1])

    snapshots = load_snapshots(SNAPSHOT_PATH)
    if not snapshots:
        print("[INFO] 尚无因子快照数据。实盘交易开始后会自动记录。")
        return

    trades = load_trades(DB_PATH)
    if not trades:
        print("[INFO] 尚无已平仓交易数据。")
        return

    matched = match_snapshots_to_trades(snapshots, trades)
    analyze_ic(matched, min_trades)


if __name__ == '__main__':
    main()
