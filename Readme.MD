# Trading Bot with OANDA API

This repository contains a simple trading bot implemented in Python using the OANDA API. The bot is designed to execute trades based on a predefined strategy using historical market data.

## Getting Started

These instructions will help you set up and run the trading bot on your local machine.

### Prerequisites

- Python 3.x
- [pip](https://pip.pypa.io/en/stable/installation/)
- OANDA API Access Token
- OANDA Account ID

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/trading-bot.git
Install dependencies:

    pip install -r requirements.txt

Create a config.py file in the project root with your OANDA API access token and account ID:

python
Copy code
# config.py
    
    # OANDA API access token
    access_token = "YOUR_OANDA_ACCESS_TOKEN"
    # OANDA account ID
    accountID = "YOUR_OANDA_ACCOUNT_ID"


# Usage
Run the trading bot script:

    python main.py
This will execute the trading job using historical market data and print the results.

<!-- Uncomment the following section if you want to schedule the trading job -->
<!-- ### Scheduling the Trading Job

To schedule the trading job to run automatically at specified intervals, uncomment the relevant code in `main.py`. Adjust the cron schedule according to your preferences. -->
Strategy
The trading bot uses a simple strategy based on bearish and bullish patterns in the market data.

Signals
Bearish Pattern: Signal 1
Bullish Pattern: Signal 2
No Clear Pattern: Signal 0
Trade Execution
The bot executes market orders with predefined stop-loss and take-profit levels based on the generated signals.

# Disclaimer
Trading involves risk, and past performance is not indicative of future results. Use this trading bot at your own risk.

# License
This project is licensed under the MIT License - see the LICENSE file for details.
