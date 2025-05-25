# Simplified Trading Bot

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
```
## Usage
Clone/download the repository.

Run the bot script:
```bash
python basic_bot.py
```
When prompted, enter your Binance Futures Testnet API key and secret.

Leave blank to use mock mode (no real API calls).

Follow the CLI menu to place orders or view order history.

## Notes
The bot connects to Binance Futures Testnet API if valid API keys are provided.

OCO orders are simulated as Binance Futures Testnet API does not natively support OCO orders.

Logging details can be found in trading_bot.log.


