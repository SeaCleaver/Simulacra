# Integration test for backtester.py: wires OrderBook -> MatchingEngine ->
# Portfolio -> MeanReversionStrategy -> Backtester and runs a small event feed.
# Structural assertions only -- no hand-computed PnL.

import pytest

from order import Order, BUY, SELL, LIMIT
from order_book import OrderBook
from matching_engine import MatchingEngine
from portfolio import Portfolio
from mean_reversion import MeanReversionStrategy
from backtester import Backtester


def test_backtest_runs_and_reports_structurally():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    portfolio = Portfolio(trader_id=1001, initial_cash=10000)
    # Large lookback keeps the strategy flat: the test stays structural rather
    # than depending on strategy-generated trades.
    strategy = MeanReversionStrategy(
        trader_id=1001, lookback=100, threshold=0.5, quantity=10
    )
    backtester = Backtester(engine, portfolio, strategy)

    # Resting orders forming a real spread (asks above bids) so they do not
    # all immediately cross each other.
    events = [
        Order(10000001, 2001, "AAPL", SELL, LIMIT, 101.00, 10, 1),
        Order(10000002, 2002, "AAPL", SELL, LIMIT, 102.00, 10, 2),
        Order(10000003, 2003, "AAPL", BUY,  LIMIT,  99.00, 10, 3),
        Order(10000004, 2004, "AAPL", BUY,  LIMIT,  98.00, 10, 4),
    ]

    backtester.run(events)

    assert len(backtester.pnl_history) == len(events)

    results = backtester.get_results()
    assert isinstance(results, dict)
    assert set(results.keys()) == {"pnl", "trades", "positions"}
