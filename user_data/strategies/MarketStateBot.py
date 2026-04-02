"""
MarketStateBot - Telegram 宏观状态控制机器人
=============================================
独立运行的轻量脚本，监听 Telegram 命令控制 CryptoV8 策略的宏观开关

命令：
  /状态        查看当前市场状态
  /趋势        设置为趋势市（策略全开）
  /横盘        设置为横盘市（ADX门槛提高，仓位减半）
  /暂停        暂停所有新入场（黑天鹅模式）
  /帮助        显示所有命令

用法：
  python /freqtrade/user_data/strategies/MarketStateBot.py
"""

import json
import os
import asyncio
import logging
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── 配置（从环境变量读取，和 Freqtrade 共用）──
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
STATE_FILE = "/freqtrade/user_data/market_state.json"

STATE_LABELS = {
    "trend": "🟢 趋势市（策略全开）",
    "range": "🟡 横盘市（ADX门槛+7，信号减少）",
    "pause": "🔴 暂停（不开新仓，现有仓位正常管理）",
}


def write_state(state: str, note: str = ""):
    data = {
        "state": state,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "note": note
    }
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"市场状态已更新: {state}")


def read_state() -> dict:
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {"state": "trend", "updated_at": "未设置", "note": ""}


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data  = read_state()
    state = data.get("state", "trend")
    label = STATE_LABELS.get(state, state)
    updated = data.get("updated_at", "未知")
    note    = data.get("note", "")
    msg = f"📊 *当前市场状态*\n\n{label}\n\n🕐 更新时间: {updated[:19]}"
    if note:
        msg += f"\n📝 备注: {note}"
    await update.message.reply_text(msg, parse_mode="Markdown")


async def cmd_trend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note = " ".join(context.args) if context.args else ""
    write_state("trend", note)
    await update.message.reply_text(
        f"✅ *已切换到趋势市模式*\n\n"
        f"策略全开，多空信号正常执行\n"
        f"适用场景：BTC 明确趋势、特朗普政策利好、ETF资金入场\n"
        + (f"备注：{note}" if note else ""),
        parse_mode="Markdown"
    )


async def cmd_range(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note = " ".join(context.args) if context.args else ""
    write_state("range", note)
    await update.message.reply_text(
        f"⚠️ *已切换到横盘市模式*\n\n"
        f"ADX 门槛提高，减少假突破信号\n"
        f"适用场景：方向不明、Fed 会议前观望、2023年那种缓慢筑底\n"
        + (f"备注：{note}" if note else ""),
        parse_mode="Markdown"
    )


async def cmd_pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    note = " ".join(context.args) if context.args else ""
    write_state("pause", note)
    await update.message.reply_text(
        f"🚨 *已暂停策略入场*\n\n"
        f"不再开新仓，现有仓位正常止盈止损\n"
        f"适用场景：LUNA崩盘、FTX暴雷、特朗普突发推文、重大黑天鹅\n"
        + (f"备注：{note}" if note else ""),
        parse_mode="Markdown"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *CryptoV8 宏观状态控制*\n\n"
        "/状态  — 查看当前状态\n"
        "/趋势  — 趋势市，策略全开\n"
        "/横盘  — 横盘市，ADX门槛提高\n"
        "/暂停  — 黑天鹅，停止开新仓\n\n"
        "可以在命令后加备注，例如：\n"
        "`/暂停 特朗普推文暴跌`\n"
        "`/趋势 BTC突破100k，机构入场`",
        parse_mode="Markdown"
    )


def main():
    if not TELEGRAM_TOKEN:
        print("错误：需要设置 TELEGRAM_TOKEN 环境变量")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # 中文命令
    app.add_handler(CommandHandler("状态", cmd_status))
    app.add_handler(CommandHandler("趋势", cmd_trend))
    app.add_handler(CommandHandler("横盘", cmd_range))
    app.add_handler(CommandHandler("暂停", cmd_pause))
    app.add_handler(CommandHandler("帮助", cmd_help))
    # 英文备用
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("trend",  cmd_trend))
    app.add_handler(CommandHandler("range",  cmd_range))
    app.add_handler(CommandHandler("pause",  cmd_pause))
    app.add_handler(CommandHandler("help",   cmd_help))

    print("✅ MarketStateBot 已启动，等待 Telegram 命令...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
