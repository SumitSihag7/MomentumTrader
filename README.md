# MomentumTrader 

**MomentumTrader** is an algorithmic backtesting engine built in Python to evaluate trend-following and momentum trading strategies across major equities.

## Strategy Overview
This backtester uses a dual-indicator strategy to generate robust Buy, Hold, and Sell signals:
1. **Simple Moving Average Crossover:** Uses a Golden Cross approach (10-day SMA > 50-day SMA) to identify upward price trends.
2. **Relative Strength Index (RSI) Filter:** Ensures the asset is not overbought or oversold by requiring the 14-day RSI to sit comfortably between 30 and 70.

The strategy acts defensively, minimizing Maximum Drawdowns by holding cash when momentum weakens.

## Features
* **Modular Engine:** The core mathematical logic is cleanly separated into an object-oriented Python module (`momentum_strategy.py`).
* **Jupyter Dashboard:** Easily run backtests and visualize interactive cumulative return charts directly within `frosthack.ipynb`.
* **Realistic Metrics:** Calculates standard quantitative finance metrics including Annualized Returns and Peak-to-Trough Drawdowns to compare strategy performance directly against a Buy & Hold baseline.

## Quick Start
1. Ensure your virtual environment is active and dependencies (`pandas`, `numpy`, `matplotlib`, `ta`) are installed.
2. Open `frosthack.ipynb` in your IDE or via a Jupyter server.
3. Click **Run All** to execute the backtests on the provided 10-year historical datasets (Apple, Facebook, Tesla, JP Morgan, Amazon).

---
*Disclaimer: This repository is for educational and backtesting purposes only. Past performance does not guarantee future results. This is not financial advice.*
