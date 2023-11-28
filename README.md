# Trading Bot with OANDA API

Automated trading bot using OANDA API with a simple strategy for executing market orders based on historical data patterns. 🤖💹 This repository contains a trading bot implemented in Python using the OANDA API. The bot is designed to execute trades based on a predefined strategy using historical market data.

## Getting Started

These instructions will help you set up and run the trading bot on your local machine.

### Prerequisites

- Python 3.x
- pip
- OANDA API Access Token
- OANDA Account ID

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/trading-bot.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a config.py file in the project root with your OANDA API access token and account ID:

    ```python
    # config.py

    # OANDA API access token
    access_token = "YOUR_OANDA_ACCESS_TOKEN"
    # OANDA account ID
    accountID = "YOUR_OANDA_ACCOUNT_ID"
    ```

### Usage

Run the trading bot script:

    ```python main.py
   
This will execute the trading job using historical market data and print the results.

### New Features
Refined Front End:
The trading bot now features a refined front end with a professional and user-friendly interface. Users can select currency pairs from a dropdown menu or enter their own pair.

### Extended Currency Pairs:
The dropdown menu includes a selection of popular currency pairs. Users can also choose "Enter Your Own Pair" and input a custom currency pair.

### Strategy
The trading bot uses a simple strategy based on bearish and bullish patterns in the market data.

### Signals:
    ```
      Bearish Pattern: Signal 1
      Bullish Pattern: Signal 2
      No Clear Pattern: Signal 0

### Trade Execution
The bot executes market orders with predefined stop-loss and take-profit levels based on the generated signals.

### Disclaimer
Trading involves risk, and past performance is not indicative of future results. Use this trading bot at your own risk.

### License
This project is licensed under the MIT License - see the LICENSE file for details.