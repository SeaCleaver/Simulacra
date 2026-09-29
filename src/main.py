# sets everything up, runs the backtest, writes results
# test writing may reference this file
# remember to change names of write output files so as to not overwrite the 
# main file

import pandas as pd
import matplotlib.pyplot as plt

from order import Order, BUY, SELL, LIMIT
from order_book import OrderBook
from matching_engine import MatchingEngine
from portfolio import Portfolio
from trend_following import TrendFollowingStrategy
from backtester import Backtester

# instantiate objects
book = OrderBook("AAPL")
engine = MatchingEngine(book)
portfolio = Portfolio(trader_id=1001, initial_cash=10000)
strategy = TrendFollowingStrategy(trader_id=1001, lookback=5, quantity=10)
backtester = Backtester(engine, portfolio, strategy)

# insert market feed (add more events if needed)
events = [
    Order(10000001, 2001, "AAPL", SELL, LIMIT, 100.00, 10, 1),
    Order(10000002, 2002, "AAPL", BUY,  LIMIT, 100.00, 10, 2),
]

# run backtest
backtester.run(events)

# WRITE outputs into trades.csv
trades_data = [
    {"trade_id": t.trade_id, "symbol": t.symbol, "price": t.price,
     "quantity": t.quantity, "timestamp": t.timestamp}
    for t in portfolio.trades
]
pd.DataFrame(trades_data).to_csv("../results/trades.csv", index=False)

# pnl.csv
pd.DataFrame({"pnl": backtester.pnl_history}).to_csv("../results/pnl.csv", index=False)

# pnl_chart.png
plt.plot(backtester.pnl_history)
plt.xlabel("Step")
plt.ylabel("Realised PnL")
plt.title("Strategy PnL Over Time")
plt.savefig("../results/pnl_chart.png")

# print summary
print(backtester.get_results())