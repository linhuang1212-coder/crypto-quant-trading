#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V4 三阶段回测实验结果自动分析脚本。

在阶段1/2/3 CSV 生成后运行，输出 Markdown 报告到 experiment_results/v4_analysis.md。

Usage:
    python user_data/scripts/analyze_v4.py

仅使用标准库；支持本地仓库路径与 Docker 内 /freqtrade 路径。
"""
from __future__ import annotations

import csv
import json
import os
import statistics
from collections import defaultdict
from typing import Any

# ---------------------------------------------------------------------------
# 路径：Docker 内为 /freqtrade，本地为仓库根（scripts 的上两级再上 user_data 的父级）
# ---------------------------------------------------------------------------
if os.path.exists("/freqtrade/user_data"):
    BASE = "/freqtrade"
else:
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESULTS_CSV = os.path.join(BASE, "user_data", "experiment_results", "v4_results.csv")
YEARLY_CSV = os.path.join(BASE, "user_data", "experiment_results", "v4_yearly.csv")
WALKFORWARD_CSV = os.path.join(BASE, "user_data", "experiment_results", "v4_walkforward.csv")
REPORT_MD = os.path.join(BASE, "user_data", "experiment_results", "v4_analysis.md")

# ---------------------------------------------------------------------------
# 从统一门控配置加载所有阈值（单一真相源）
# ---------------------------------------------------------------------------
GATES_JSON = os.path.join(BASE, "user_data", "configs", "experiment_gates.json")

def _load_gates() -> dict:
    with open(GATES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

_GATES = _load_gates()

BASELINE_FULL = {
    "sharpe": _GATES["baseline"]["sharpe"],
    "profit_factor": _GATES["baseline"]["profit_factor"],
    "max_drawdown_pct": _GATES["baseline"]["max_drawdown_pct"],
    "tot_profit_pct": _GATES["baseline"]["tot_profit_pct"],
    "trades": _GATES["baseline"]["trades"],
}
BASELINE_YEARLY_NOTE = _GATES.get("baseline_yearly_note", "")

STAGE1_MIN_SHARPE = _GATES["stage1"]["min_sharpe"]
STAGE1_MIN_PF = _GATES["stage1"]["min_pf"]
STAGE1_MIN_TRADES = _GATES["stage1"]["min_trades"]
STAGE1_MAX_DD = _GATES["stage1"]["max_dd"]

STAGE2_MAX_CV_ACCEPTABLE = _GATES["stage2"]["max_cv_acceptable"]
STAGE2_MAX_CV_STABLE = _GATES["stage2"]["max_cv_stable"]
STAGE2_MIN_PROFITABLE_YEARS_ACCEPTABLE = _GATES["stage2"]["min_profitable_years"]

STAGE3_PASS_MIN_OOS = _GATES["stage3"]["min_oos"]
STRONG_REC_MIN_OOS = _GATES["stage3"]["strong_rec_min_oos"]

NEIGHBOR_SMOOTH_STD = _GATES["analysis"]["neighbor_smooth_std"]
NEIGHBOR_NORMAL_STD_MAX = _GATES["analysis"]["neighbor_normal_std_max"]
OVERFIT_SPIKE_DELTA = _GATES["analysis"]["overfit_spike_delta"]


def _key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (str(row.get("strategy", "")), str(row.get("group", "")), str(row.get("name", "")))


def _f(x: Any, default: float = 0.0) -> float:
    try:
        if x is None or str(x).strip() == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


def _i(x: Any, default: int = 0) -> int:
    try:
        if x is None or str(x).strip() == "":
            return default
        return int(float(x))
    except (TypeError, ValueError):
        return default


def load_csv(path: str) -> list[dict[str, str]] | None:
    if not os.path.isfile(path):
        return None
    rows: list[dict[str, str]] = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({k: (v if v is not None else "") for k, v in row.items()})
    return rows


def normalize_phase(phase: str) -> str:
    p = (phase or "").strip().lower()
    if "train" in p or "训练" in p:
        return "train"
    if "test" in p or "测试" in p or "oos" in p or "valid" in p:
        return "test"
    return p or "unknown"


def stage1_pass(row: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    ok = True
    sh = _f(row.get("sharpe"))
    pf = _f(row.get("profit_factor"))
    tr = _i(row.get("trades"))
    dd = _f(row.get("max_drawdown_pct"))
    if sh < STAGE1_MIN_SHARPE:
        ok = False
        reasons.append(f"Sharpe<{STAGE1_MIN_SHARPE}")
    if pf < STAGE1_MIN_PF:
        ok = False
        reasons.append(f"PF<{STAGE1_MIN_PF}")
    if tr < STAGE1_MIN_TRADES:
        ok = False
        reasons.append(f"交易数<{STAGE1_MIN_TRADES}")
    if dd > STAGE1_MAX_DD:
        ok = False
        reasons.append(f"回撤>{STAGE1_MAX_DD}%")
    return ok, reasons


def beats_baseline_full(row: dict[str, Any]) -> dict[str, bool]:
    return {
        "sharpe": _f(row.get("sharpe")) >= BASELINE_FULL["sharpe"],
        "profit_factor": _f(row.get("profit_factor")) >= BASELINE_FULL["profit_factor"],
        "max_drawdown_pct": _f(row.get("max_drawdown_pct")) <= BASELINE_FULL["max_drawdown_pct"],
        "tot_profit_pct": _f(row.get("tot_profit_pct")) >= BASELINE_FULL["tot_profit_pct"],
        "trades": _i(row.get("trades")) >= BASELINE_FULL["trades"],
    }


def neighbor_std_label(std: float) -> str:
    if std < NEIGHBOR_SMOOTH_STD:
        return "平滑"
    if std <= NEIGHBOR_NORMAL_STD_MAX:
        return "正常"
    return "敏感"


def yearly_consistency_label(cv: float, profit_years: int, total_years: int) -> str:
    if total_years <= 0:
        return "无数据"
    need_accept = max(1, min(total_years, STAGE2_MIN_PROFITABLE_YEARS_ACCEPTABLE))
    if total_years < 6:
        need_accept = max(1, total_years - 1)
    stable_profit = profit_years >= total_years
    acceptable_profit = profit_years >= need_accept
    if cv < STAGE2_MAX_CV_STABLE and stable_profit:
        return "稳定"
    if cv < STAGE2_MAX_CV_ACCEPTABLE and acceptable_profit:
        return "可接受"
    return "不稳定"


def stage2_pass_from_yearly(
    cv: float,
    profit_years: int,
    total_years: int,
    label: str,
) -> bool:
    if total_years <= 0:
        return False
    return label in {"稳定", "可接受"}


def wf_overfit_label(oos: float | None) -> str:
    if oos is None:
        return "无数据"
    if oos > 0.8:
        return "无过拟合"
    if oos >= 0.5:
        return "轻微"
    return "严重"


def sharpe_pstdev(vals: list[float]) -> float:
    if len(vals) < 2:
        return 0.0
    return float(statistics.pstdev(vals))


def build_yearly_index(yearly_rows: list[dict[str, str]] | None) -> dict[tuple[str, str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    if not yearly_rows:
        return out
    for row in yearly_rows:
        k = _key(row)
        y = str(row.get("year", "")).strip()
        out[k].append(
            {
                "year": y,
                "timerange": row.get("timerange", ""),
                "trades": _i(row.get("trades")),
                "tot_profit_pct": _f(row.get("tot_profit_pct")),
                "sharpe": _f(row.get("sharpe")),
                "profit_factor": _f(row.get("profit_factor")),
                "max_drawdown_pct": _f(row.get("max_drawdown_pct")),
                "win_rate": _f(row.get("win_rate")),
                "cagr": _f(row.get("cagr")),
                "sortino": _f(row.get("sortino")),
            }
        )
    return out


def yearly_metrics_for_key(
    items: list[dict[str, Any]],
) -> tuple[float, float, float, int, int, float]:
    """返回 mean_sharpe, std_sharpe, cv, profit_years, total_years, sharpe_2022"""
    if not items:
        return 0.0, 0.0, float("inf"), 0, 0, float("nan")
    sharpes = [it["sharpe"] for it in items]
    mean_s = float(statistics.mean(sharpes)) if sharpes else 0.0
    std_s = float(statistics.pstdev(sharpes)) if len(sharpes) > 1 else 0.0
    denom = abs(mean_s) if abs(mean_s) > 1e-9 else float("inf")
    cv = std_s / denom if denom != float("inf") else float("inf")
    profit_years = sum(1 for it in items if it["tot_profit_pct"] > 0)
    total_years = len(items)
    s2022 = float("nan")
    for it in items:
        y = it["year"]
        if y == "2022" or y.startswith("2022"):
            s2022 = it["sharpe"]
            break
    return mean_s, std_s, cv, profit_years, total_years, s2022


def build_walkforward_stats(
    wf_rows: list[dict[str, str]] | None,
) -> dict[tuple[str, str, str], dict[str, Any]]:
    out: dict[tuple[str, str, str], dict[str, Any]] = defaultdict(
        lambda: {
            "windows": defaultdict(lambda: {"train": None, "test": None}),
        }
    )
    if not wf_rows:
        return {}
    for row in wf_rows:
        k = _key(row)
        w = str(row.get("window", "")).strip()
        ph = normalize_phase(str(row.get("phase", "")))
        block = out[k]["windows"][w]
        entry = {
            "sharpe": _f(row.get("sharpe")),
            "profit_factor": _f(row.get("profit_factor")),
            "tot_profit_pct": _f(row.get("tot_profit_pct")),
            "trades": _i(row.get("trades")),
            "timerange": row.get("timerange", ""),
        }
        if ph == "train":
            block["train"] = entry
        elif ph == "test":
            block["test"] = entry
    # 聚合为平均训练/测试指标
    result: dict[tuple[str, str, str], dict[str, Any]] = {}
    for k, payload in out.items():
        trains: list[float] = []
        tests: list[float] = []
        trains_pf: list[float] = []
        tests_pf: list[float] = []
        for _w, pr in payload["windows"].items():
            tr = pr.get("train")
            te = pr.get("test")
            if tr:
                trains.append(tr["sharpe"])
                trains_pf.append(tr["profit_factor"])
            if te:
                tests.append(te["sharpe"])
                tests_pf.append(te["profit_factor"])
        avg_train = float(statistics.mean(trains)) if trains else float("nan")
        avg_test = float(statistics.mean(tests)) if tests else float("nan")
        avg_train_pf = float(statistics.mean(trains_pf)) if trains_pf else float("nan")
        avg_test_pf = float(statistics.mean(tests_pf)) if tests_pf else float("nan")
        oos = None
        if trains and tests and abs(avg_train) > 1e-9:
            oos = avg_test / avg_train
        pf_decay = None
        if trains_pf and tests_pf and abs(avg_train_pf) > 1e-9:
            pf_decay = avg_test_pf / avg_train_pf
        result[k] = {
            "avg_train_sharpe": avg_train,
            "avg_test_sharpe": avg_test,
            "oos_ratio": oos,
            "avg_train_pf": avg_train_pf,
            "avg_test_pf": avg_test_pf,
            "pf_decay": pf_decay,
            "n_windows": len(payload["windows"]),
        }
    return result


def group_neighbor_analysis(
    results_rows: list[dict[str, Any]],
) -> tuple[dict[tuple[str, str], float], dict[tuple[str, str, str], list[str]]]:
    """按 (strategy, group) 计算 Sharpe 标准差；按排序后的 name 检测孤立尖峰。"""
    by_sg: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for r in results_rows:
        by_sg[(str(r["strategy"]), str(r["group"]))].append(r)

    std_map: dict[tuple[str, str], float] = {}
    spike_flags: dict[tuple[str, str, str], list[str]] = defaultdict(list)

    for sg, lst in by_sg.items():
        sharpes = [_f(x.get("sharpe")) for x in lst]
        std_map[sg] = sharpe_pstdev(sharpes)
        sorted_lst = sorted(lst, key=lambda x: str(x.get("name", "")))
        n = len(sorted_lst)
        for i in range(n):
            s_i = _f(sorted_lst[i].get("sharpe"))
            neighbors: list[float] = []
            if i > 0:
                neighbors.append(_f(sorted_lst[i - 1].get("sharpe")))
            if i < n - 1:
                neighbors.append(_f(sorted_lst[i + 1].get("sharpe")))
            if len(neighbors) >= 1:
                mx = max(neighbors)
                if s_i - mx > OVERFIT_SPIKE_DELTA:
                    kk = _key(sorted_lst[i])
                    spike_flags[kk].append("可能过拟合（Sharpe 显著高于相邻变体）")
    return std_map, spike_flags


def fmt_num(x: Any, nd: int = 2, empty: str = "—") -> str:
    if x is None:
        return empty
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return empty
    if xf != xf:  # NaN
        return empty
    return f"{xf:.{nd}f}"


def summarize_baseline_flags(flags: dict[str, bool]) -> str:
    parts = []
    mapping = [
        ("Sharpe", "sharpe"),
        ("PF", "profit_factor"),
        ("回撤", "max_drawdown_pct"),
        ("利润%", "tot_profit_pct"),
        ("交易数", "trades"),
    ]
    for label, k in mapping:
        parts.append(f"{label}:{'✓' if flags[k] else '×'}")
    return " ".join(parts)


def main() -> None:
    lines: list[str] = []
    lines.append("# V4 三阶段回测分析报告")
    lines.append("")
    lines.append(f"- 生成路径: `{REPORT_MD}`")
    lines.append(f"- 数据根目录: `{BASE}`")
    lines.append("")

    raw_results = load_csv(RESULTS_CSV)
    raw_yearly = load_csv(YEARLY_CSV)
    raw_wf = load_csv(WALKFORWARD_CSV)

    missing: list[str] = []
    if raw_results is None:
        missing.append(f"未找到 `{RESULTS_CSV}`，已跳过阶段1相关分析。")
    if raw_yearly is None:
        missing.append(f"未找到 `{YEARLY_CSV}`，已跳过阶段2/分年度与部分综合结论。")
    if raw_wf is None:
        missing.append(f"未找到 `{WALKFORWARD_CSV}`，已跳过 Walk-Forward 与部分综合结论。")

    if missing:
        lines.append("## 数据文件状态")
        for m in missing:
            lines.append(f"- {m}")
        lines.append("")

    # 解析阶段1
    results: list[dict[str, Any]] = []
    if raw_results:
        for row in raw_results:
            r = dict(row)
            r["trades"] = _i(row.get("trades"))
            for k in (
                "avg_profit_pct",
                "tot_profit_usdt",
                "tot_profit_pct",
                "sharpe",
                "profit_factor",
                "max_drawdown_pct",
                "win_rate",
                "cagr",
                "sortino",
            ):
                r[k] = _f(row.get(k))
            results.append(r)

    yearly_idx = build_yearly_index(raw_yearly)
    wf_stats = build_walkforward_stats(raw_wf)
    std_map, spike_flags = group_neighbor_analysis(results) if results else ({}, {})

    # --- 1. 全样本 Top 20 ---
    lines.append("## 1. 全样本排名（Top 20，按 Sharpe 降序）")
    lines.append("")
    if not results:
        lines.append("（无阶段1数据）")
        lines.append("")
    else:
        lines.append(
            f"基线参考: Sharpe **{BASELINE_FULL['sharpe']}**, PF **{BASELINE_FULL['profit_factor']}**, "
            f"最大回撤 **{BASELINE_FULL['max_drawdown_pct']}%**, 总利润 **{BASELINE_FULL['tot_profit_pct']}%**, "
            f"交易数 **{BASELINE_FULL['trades']}**。"
        )
        lines.append("")
        top = sorted(results, key=lambda x: _f(x.get("sharpe")), reverse=True)[:20]
        lines.append(
            "| 排名 | strategy | group | name | Sharpe | PF | 利润% | 回撤% | 交易数 | 超越基线(分项) |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for i, r in enumerate(top, 1):
            flags = beats_baseline_full(r)
            flag_s = summarize_baseline_flags(flags)
            params_short = (r.get("params") or "")[:40]
            if len(str(r.get("params") or "")) > 40:
                params_short += "…"
            lines.append(
                f"| {i} | {r.get('strategy','')} | {r.get('group','')} | {r.get('name','')} | "
                f"{fmt_num(r.get('sharpe'))} | {fmt_num(r.get('profit_factor'))} | "
                f"{fmt_num(r.get('tot_profit_pct'), 1)} | {fmt_num(r.get('max_drawdown_pct'), 1)} | "
                f"{r.get('trades','')} | {flag_s} |"
            )
        lines.append("")
        lines.append("<details><summary>Top20 的 params 摘要（展开）</summary>")
        lines.append("")
        lines.append("| 排名 | params |")
        lines.append("| --- | --- |")
        for i, r in enumerate(top, 1):
            p = r.get("params") or ""
            lines.append(f"| {i} | `{p}` |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    # --- 2. 分组汇总 ---
    lines.append("## 2. 分组汇总")
    lines.append("")
    if not results:
        lines.append("（无阶段1数据）")
        lines.append("")
    else:
        by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in results:
            by_group[str(r.get("group", ""))].append(r)

        lines.append(
            "| group | 策略数 | 阶段1通过率 | 组均Sharpe | 最优 name | 最优Sharpe | "
            "分年度验证 | Walk-Forward | 邻域std标签 | 结论 |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")

        for g in sorted(by_group.keys(), key=lambda x: (x == "", x)):
            lst = by_group[g]
            passed = [x for x in lst if stage1_pass(x)[0]]
            rate = len(passed) / len(lst) if lst else 0.0
            mean_sh = float(statistics.mean([_f(x.get("sharpe")) for x in lst])) if lst else 0.0
            best = max(lst, key=lambda x: _f(x.get("sharpe")))
            bk = _key(best)
            sg = (str(best.get("strategy")), g)
            std_g = std_map.get(sg, 0.0)
            std_lbl = neighbor_std_label(std_g)

            y_items = yearly_idx.get(bk, [])
            _, _, cv, py, ty, s2022 = yearly_metrics_for_key(y_items)
            y_label = yearly_consistency_label(cv, py, ty) if y_items else "无年度数据"
            s2_ok = stage2_pass_from_yearly(cv, py, ty, y_label) if y_items else False

            wf = wf_stats.get(bk, {})
            oos = wf.get("oos_ratio")
            wf_lbl = wf_overfit_label(oos) if wf else "无WF数据"
            s3_ok = bool(wf) and oos is not None and oos >= STAGE3_PASS_MIN_OOS and _f(wf.get("avg_test_sharpe")) > 0

            # 组结论
            if not passed:
                conclusion = "放弃"
            elif s2_ok and s3_ok and _f(best.get("sharpe")) >= 1.0:
                conclusion = "推荐"
            elif s2_ok or s3_ok or _f(best.get("sharpe")) >= STAGE1_MIN_SHARPE + 0.3:
                conclusion = "有潜力"
            else:
                conclusion = "放弃"

            y_disp = f"{y_label} (CV={fmt_num(cv)}, {py}/{ty}年盈利)" if y_items else "—"
            wf_disp = f"{wf_lbl} (OOS={fmt_num(oos) if oos is not None else '—'})" if wf else "—"

            lines.append(
                f"| {g} | {len(lst)} | {rate:.0%} | {fmt_num(mean_sh)} | {best.get('name','')} | "
                f"{fmt_num(best.get('sharpe'))} | {y_disp} | {wf_disp} | {std_lbl} ({fmt_num(std_g)}) | {conclusion} |"
            )
        lines.append("")
        lines.append(f"> 分年度参考：{BASELINE_YEARLY_NOTE}")
        lines.append("")

    # --- 3. 参数邻域稳定性 ---
    lines.append("## 3. 参数邻域稳定性（阶段1，按 group × strategy）")
    lines.append("")
    if not results:
        lines.append("（无阶段1数据）")
        lines.append("")
    else:
        lines.append(
            "在同一 `strategy`+`group` 内，对所有变体的 Sharpe 计算总体标准差；"
            "并按 `name` 字典序相邻检测尖峰（高于邻居最大值超过 0.3）。"
        )
        lines.append("")
        by_sg: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for r in results:
            by_sg[(str(r.get("strategy")), str(r.get("group")))].append(r)
        lines.append("| strategy | group | 变体数 | Sharpe std | 稳定性 | 尖峰标记(若有) |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for (st, g) in sorted(by_sg.keys(), key=lambda x: (x[0], x[1])):
            lst = by_sg[(st, g)]
            sharpes = [_f(x.get("sharpe")) for x in lst]
            sd = sharpe_pstdev(sharpes)
            lbl = neighbor_std_label(sd)
            spikes = []
            for r in lst:
                kk = _key(r)
                if spike_flags.get(kk):
                    spikes.append(f"{r.get('name')}: {','.join(spike_flags[kk])}")
            sp = "; ".join(spikes) if spikes else "—"
            lines.append(f"| {st} | {g} | {len(lst)} | {fmt_num(sd)} | {lbl} | {sp} |")
        lines.append("")

    # --- 4. 分年度一致性 ---
    lines.append("## 4. 分年度一致性（仅阶段1已通过门控的候选）")
    lines.append("")
    if raw_yearly is None:
        lines.append("（无年度 CSV）")
        lines.append("")
    elif not results:
        lines.append("（无阶段1数据）")
        lines.append("")
    else:
        candidates = [r for r in results if stage1_pass(r)[0]]
        lines.append(
            f"规则：**稳定** = CV < {STAGE2_MAX_CV_STABLE} 且全年份盈利；"
            f"**可接受** = CV < {STAGE2_MAX_CV_ACCEPTABLE} 且盈利年份≥ max(1, 总年数-1)；否则 **不稳定**。"
        )
        lines.append("")
        lines.append(
            "| strategy | group | name | 全样本Sharpe | 年份数 | 盈利年数 | CV | 2022 Sharpe | 标签 | 阶段2通过 |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in sorted(candidates, key=lambda x: (-_f(x.get("sharpe")), str(x.get("group")), str(x.get("name")))):
            k = _key(r)
            items = yearly_idx.get(k, [])
            if not items:
                lines.append(
                    f"| {r.get('strategy')} | {r.get('group')} | {r.get('name')} | {fmt_num(r.get('sharpe'))} | "
                    f"0 | 0 | — | — | 无年度行 | 否 |"
                )
                continue
            _, _, cv, py, ty, s2022 = yearly_metrics_for_key(items)
            label = yearly_consistency_label(cv, py, ty)
            s2 = stage2_pass_from_yearly(cv, py, ty, label)
            lines.append(
                f"| {r.get('strategy')} | {r.get('group')} | {r.get('name')} | {fmt_num(r.get('sharpe'))} | "
                f"{ty} | {py} | {fmt_num(cv)} | {fmt_num(s2022)} | {label} | {'是' if s2 else '否'} |"
            )
        lines.append("")

    # --- 5. Walk-Forward ---
    lines.append("## 5. Walk-Forward 过拟合检测（对阶段2已通过门控的候选）")
    lines.append("")
    if raw_wf is None:
        lines.append("（无 Walk-Forward CSV）")
        lines.append("")
    elif not results or raw_yearly is None:
        lines.append("（缺少阶段1或阶段2数据，无法筛选候选）")
        lines.append("")
    else:
        lines.append(
            "OOS Ratio = 平均(测试期 Sharpe) / 平均(训练期 Sharpe)；"
            "PF Decay = 平均(测试期 PF) / 平均(训练期 PF)。"
        )
        lines.append("")
        lines.append(
            "| strategy | group | name | 均训练Sharpe | 均测试Sharpe | OOS | PF Decay | 过拟合标签 |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for r in results:
            if not stage1_pass(r)[0]:
                continue
            k = _key(r)
            items = yearly_idx.get(k, [])
            if items:
                _, _, cv, py, ty, _ = yearly_metrics_for_key(items)
                y_label = yearly_consistency_label(cv, py, ty)
                if not stage2_pass_from_yearly(cv, py, ty, y_label):
                    continue
            else:
                continue
            wf = wf_stats.get(k, {})
            if not wf:
                lines.append(
                    f"| {r.get('strategy')} | {r.get('group')} | {r.get('name')} | — | — | — | — | 无WF行 |"
                )
                continue
            oos = wf.get("oos_ratio")
            pfd = wf.get("pf_decay")
            lines.append(
                f"| {r.get('strategy')} | {r.get('group')} | {r.get('name')} | "
                f"{fmt_num(wf.get('avg_train_sharpe'))} | {fmt_num(wf.get('avg_test_sharpe'))} | "
                f"{fmt_num(oos) if oos is not None else '—'} | {fmt_num(pfd) if pfd is not None else '—'} | "
                f"{wf_overfit_label(oos)} |"
            )
        lines.append("")

    # --- 6. 最终推荐 ---
    lines.append("## 6. 最终推荐（综合三阶段）")
    lines.append("")
    lines.append("判定摘要：")
    lines.append(
        f"- **阶段1**：Sharpe≥{STAGE1_MIN_SHARPE}、PF≥{STAGE1_MIN_PF}、交易≥{STAGE1_MIN_TRADES}、回撤≤{STAGE1_MAX_DD}%。"
    )
    lines.append(
        f"- **阶段2**：分年度标签为「稳定」或「可接受」（见第4节）。"
    )
    lines.append(
        f"- **阶段3**：存在 WF 行且 OOS≥{STAGE3_PASS_MIN_OOS} 且平均测试 Sharpe>0；"
        f"**强烈推荐** 另要求 OOS>{STRONG_REC_MIN_OOS} 且组内邻域 Sharpe 标准差 < {NEIGHBOR_SMOOTH_STD}（平滑）。"
    )
    lines.append("")

    strong: list[str] = []
    rec: list[str] = []
    watch: list[str] = []
    drop: list[str] = []

    if results and raw_yearly is not None:
        for r in results:
            k = _key(r)
            s1, _ = stage1_pass(r)
            if not s1:
                drop.append(
                    f"- **放弃** `{k[0]}` / `{k[1]}` / `{k[2]}`：未通过阶段1"
                )
                continue
            items = yearly_idx.get(k, [])
            if not items:
                drop.append(
                    f"- **放弃** `{k[0]}` / `{k[1]}` / `{k[2]}`：无分年度数据，无法完成阶段2"
                )
                continue
            _, _, cv, py, ty, _ = yearly_metrics_for_key(items)
            y_label = yearly_consistency_label(cv, py, ty)
            s2 = stage2_pass_from_yearly(cv, py, ty, y_label)
            if not s2:
                drop.append(
                    f"- **放弃** `{k[0]}` / `{k[1]}` / `{k[2]}`：阶段2「{y_label}」"
                )
                continue

            wf = wf_stats.get(k, {}) if raw_wf is not None else {}
            oos = wf.get("oos_ratio") if wf else None
            test_sh = _f(wf.get("avg_test_sharpe")) if wf else float("nan")
            s3 = (
                bool(wf)
                and oos is not None
                and oos >= STAGE3_PASS_MIN_OOS
                and test_sh > 0
            )
            full_sh = _f(r.get("sharpe"))
            sg = (str(r.get("strategy")), str(r.get("group")))
            std_g = std_map.get(sg, 0.0)
            smooth = std_g < NEIGHBOR_SMOOTH_STD

            if not s3:
                watch.append(
                    f"- **观察** `{k[0]}` / `{k[1]}` / `{k[2]}`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS={fmt_num(oos) if oos is not None else '—'}）"
                )
                continue

            if full_sh <= 1.0:
                watch.append(
                    f"- **观察** `{k[0]}` / `{k[1]}` / `{k[2]}`：三阶段均通过，但全样本 Sharpe≤1.0（当前 {fmt_num(full_sh)}），未达「推荐」门槛"
                )
                continue

            if (
                full_sh > BASELINE_FULL["sharpe"]
                and oos is not None
                and oos > STRONG_REC_MIN_OOS
                and smooth
            ):
                strong.append(
                    f"- **强烈推荐** `{k[0]}` / `{k[1]}` / `{k[2]}`：三阶段通过，Sharpe>{BASELINE_FULL['sharpe']}，OOS>{STRONG_REC_MIN_OOS}，邻域平滑(std={fmt_num(std_g)})"
                )
            else:
                rec.append(
                    f"- **推荐** `{k[0]}` / `{k[1]}` / `{k[2]}`：三阶段通过且 Sharpe>1.0（OOS={fmt_num(oos)}）"
                )

    def emit_section(title: str, items: list[str], empty_msg: str) -> None:
        lines.append(f"### {title}")
        lines.append("")
        if not items:
            lines.append(empty_msg)
        else:
            lines.extend(items)
        lines.append("")

    emit_section("强烈推荐", strong, "（当前无候选满足全部强化条件）")
    emit_section("推荐", rec, "（当前无候选满足三阶段+Sharpe 条件）")
    emit_section("观察名单", watch, "（无）")
    emit_section("放弃/未过关", drop[:200], "（无或未加载数据）")
    if len(drop) > 200:
        lines.append(f"> 放弃条目过多，仅显示前 200 条，共 {len(drop)} 条。")
        lines.append("")

    # --- 7. 失败方向总结 ---
    lines.append("## 7. 失败方向总结（按 group，避免重复踩坑）")
    lines.append("")
    if not results:
        lines.append("（无阶段1数据）")
        lines.append("")
    else:
        by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in results:
            by_group[str(r.get("group", ""))].append(r)
        for g in sorted(by_group.keys(), key=lambda x: (x == "", x)):
            fails = [x for x in by_group[g] if not stage1_pass(x)[0]]
            if not fails:
                continue
            lines.append(f"### group `{g}`")
            lines.append("")
            for r in sorted(fails, key=lambda x: str(x.get("name"))):
                _, rs = stage1_pass(r)
                reason = "；".join(rs) if rs else "未知"
                lines.append(
                    f"- **失败** `{r.get('strategy')}` / `{r.get('name')}`：{reason} "
                    f"(Sharpe={fmt_num(r.get('sharpe'))}, PF={fmt_num(r.get('profit_factor'))}, "
                    f"交易={r.get('trades')}, 回撤%={fmt_num(r.get('max_drawdown_pct'))})"
                )
            lines.append("")

    # 附录：门控常量 JSON
    lines.append("## 附录：脚本门控参数（可复制到流水线配置）")
    lines.append("")
    cfg = {
        "STAGE1_MIN_SHARPE": STAGE1_MIN_SHARPE,
        "STAGE1_MIN_PF": STAGE1_MIN_PF,
        "STAGE1_MIN_TRADES": STAGE1_MIN_TRADES,
        "STAGE1_MAX_DD": STAGE1_MAX_DD,
        "STAGE2_MAX_CV_STABLE": STAGE2_MAX_CV_STABLE,
        "STAGE2_MAX_CV_ACCEPTABLE": STAGE2_MAX_CV_ACCEPTABLE,
        "STAGE3_PASS_MIN_OOS": STAGE3_PASS_MIN_OOS,
        "STRONG_REC_MIN_OOS": STRONG_REC_MIN_OOS,
        "NEIGHBOR_SMOOTH_STD": NEIGHBOR_SMOOTH_STD,
        "BASELINE_FULL": BASELINE_FULL,
    }
    lines.append("```json")
    lines.append(json.dumps(cfg, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")

    os.makedirs(os.path.dirname(REPORT_MD), exist_ok=True)
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote report: {REPORT_MD}")


if __name__ == "__main__":
    main()
