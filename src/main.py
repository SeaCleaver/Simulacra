# sets everything up, runs the backtest, writes results
# remember to change names of write output files to prevent overwriting other
# results

import pandas as pd
import matplotlib.pyplot as plt

from order import Order, BUY, SELL, LIMIT
from order_book import OrderBook
from matching_engine import MatchingEngine
from portfolio import Portfolio
from strategies.trend_following import TrendFollowingStrategy
from backtester import Backtester

# instantiate objects
book = OrderBook("AAPL")
engine = MatchingEngine(book)
portfolio = Portfolio(trader_id=1001, initial_cash=10000)
strategy = TrendFollowingStrategy(trader_id=1001, lookback=5, quantity=10)
backtester = Backtester(engine, portfolio, strategy)

# insert market feed (add more events if needed)
events = [
    Order(20000001, 2002, "AAPL", BUY,  LIMIT,  99.00, 10, 1),
    Order(20000002, 2001, "AAPL", SELL, LIMIT, 101.00, 10, 2),
    Order(20000003, 2001, "AAPL", SELL, LIMIT, 102.00, 10, 3),
    Order(20000004, 2001, "AAPL", SELL, LIMIT, 103.00, 10, 4),
    Order(20000005, 2001, "AAPL", SELL, LIMIT, 104.00, 10, 5),
    Order(20000006, 2001, "AAPL", SELL, LIMIT, 105.00, 10, 6),
    Order(20000007, 2001, "AAPL", SELL, LIMIT, 106.00, 10, 7),
    Order(20000008, 2002, "AAPL", BUY,  LIMIT, 101.00, 10, 8),
    Order(20000009, 2002, "AAPL", BUY,  LIMIT, 102.00, 10, 9),
    Order(20000010, 2002, "AAPL", BUY,  LIMIT, 103.00, 10, 10),
    Order(20000011, 2002, "AAPL", BUY,  LIMIT, 104.00, 10, 11),
    Order(20000012, 2003, "AAPL", SELL, LIMIT,  95.00, 40, 12),
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