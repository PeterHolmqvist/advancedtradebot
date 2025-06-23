# File: strategies/trend.py

import time
import random
from utils.telegram import send_telegram

positions = []
pnl = 0


def log(config, msg):
    print(msg)
    if config["telegram"]["enabled"]:
        send_telegram(config, msg)


def detect_trend(prices):
    if len(prices) < 3:
        return "sideways"
    if prices[-1] > prices[-2] > prices[-3]:
        return "up"
    elif prices[-1] < prices[-2] < prices[-3]:
        return "down"
    return "sideways"


def run(config):
    global pnl
    price_history = []

    for _ in range(10):
        price = simulate_price(config["grid_range"])
        price_history.append(price)
        trend = detect_trend(price_history)

        if trend == "up" and not positions:
            positions.append(price)
            log(config, f"📈 Trend UP - BUY at ${price:.2f}")

        elif trend == "down" and positions:
            entry = positions.pop()
            profit = price - entry
            pnl += profit
            log(config, f"📉 Trend DOWN - SELL at ${price:.2f} | PnL: ${profit:.2f}")

        else:
            log(config, f"😐 Trend {trend.upper()} - HOLD at ${price:.2f}")

        time.sleep(2)

    log(config, f"📊 Final PnL (Trend): ${pnl:.2f}")


def simulate_price(grid_range):
    return round(random.uniform(*grid_range), 2)
