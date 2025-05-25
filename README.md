# Simplified Crypto Trading Bot

## Overview

This project is a simplified crypto trading bot designed for Binance Futures Testnet (USDT-M) using Python. The bot supports placing market, limit, stop-limit, and OCO-style orders through a command-line interface (CLI). It includes logging for API requests, responses, and errors.

---

## Features

- Connects to Binance Futures Testnet API using provided API keys.
- Supports order types:
  - Market
  - Limit
  - Stop-Limit (bonus)
  - OCO-style orders (bonus, simulated)
- Accepts and validates user inputs via CLI.
- Outputs detailed order execution status.
- Implements logging to file (`trading_bot.log`).
- Runs in mock mode if API keys are not provided or invalid.

---

## Requirements

- Python 3.6+
- `python-binance` library

Install dependencies with:

```bash
pip install python-binance



