# File: strategies/volatility.py

import time
import random
import statistics
from utils.telegram import send_telegram

positions = []
pnl = 0


def log(config, msg):
    print(msg)
    if config["telegram"]["enabled"]:
        send_telegram(config, msg)


def compute_volatility(prices):
    if len(prices) < 2:
        return 0
    return statistics.stdev(prices)


def run(config):
    global pnl
    price_history = []

    for _ in range(10):
        price = simulate_price(config["grid_range"])
        price_history.append(price)
        vol = compute_volatility(price_history[-5:])

        if vol > config["volatility_threshold"]:
            if not positions:
                positions.append(price)
                log(config, f"📊 High Volatility (${vol:.2f}) - BUY at ${price:.2f}")
            else:
                entry = positions.pop()
                profit = price - entry
                pnl += profit
                log(config, f"📊 High Volatility (${vol:.2f}) - SELL at ${price:.2f} | PnL: ${profit:.2f}")
        else:
            log(config, f"🔍 Low Volatility (${vol:.2f}) - HOLD at ${price:.2f}")

        time.sleep(2)

    log(config, f"📈 Final PnL (Volatility): ${pnl:.2f}")


def simulate_price(grid_range):
    return round(random.uniform(*grid_range), 2)