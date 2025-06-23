# File: strategies/grid.py

import random
import time
from datetime import datetime
from utils.telegram import send_telegram

positions = {}
pnl = 0


def log(config, msg):
    print(msg)
    if config["telegram"]["enabled"]:
        send_telegram(config, msg)


def run(config):
    global pnl
    grid = generate_grid(config["grid_range"], config["grid_levels"])
    log(config, f"📊 Grid levels: {grid}")

    current_price = simulate_price(grid)

    for level in grid:
        if current_price <= level and level not in positions:
            positions[level] = current_price
            log(config, f"✅ Sim BUY at ${current_price:.2f} (Grid {level})")

        elif current_price > level and level in positions:
            buy_price = positions.pop(level)
            trade_pnl = current_price - buy_price
            pnl += trade_pnl
            log(config, f"💰 Sim SELL at ${current_price:.2f} | PnL: ${trade_pnl:.2f}")

    log(config, f"📈 Total PnL: ${pnl:.2f}")
    time.sleep(2)  # Simulate time delay for loop


def generate_grid(grid_range, levels):
    low, high = grid_range
    step = (high - low) / levels
    return [round(low + i * step, 2) for i in range(levels + 1)]


def simulate_price(grid):
    return round(random.uniform(min(grid), max(grid)), 2)