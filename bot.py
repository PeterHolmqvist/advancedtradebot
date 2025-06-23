# File: bot.py

import time
from mode_manager import ModeManager
from strategies import grid, trend, volatility
from utils.telegram import send_telegram

# Load mode and config
mm = ModeManager()
config = mm.get_config()
mode = mm.get_mode()

# Notify start
if config["telegram"]["enabled"]:
    send_telegram(config, f"🚀 Starting bot in {mode.upper()} mode for {config['pair']}")

# Strategy selector
strategy_map = {
    "grid": grid.run,
    "trend": trend.run,
    "volatility": volatility.run
}

# Run selected strategy
if mode in strategy_map:
    try:
        strategy_map[mode](config)
    except Exception as e:
        send_telegram(config, f"❌ Error in {mode} mode: {e}")
else:
    print("❌ Invalid mode in config.json")