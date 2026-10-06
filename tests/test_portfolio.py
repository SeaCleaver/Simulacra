# Tests for portfolio.py: cash/position accounting on buys and sells,
# unseen-symbol handling, non-participating trades, and realised PnL.

import pytest

from trade import Trade
from portfolio import Portfolio


TRADER_ID = 1234
INITIAL_CASH = 10000.0


@pytest.fixture
def portfolio():
    return Portfolio(trader_id=TRADER_ID, initial_cash=INITIAL_CASH)


def make_trade(buyer_id, seller_id, symbol="AAPL", price=100.0, quantity=5):
    return Trade(
        trade_id=1234567,
        symbol=symbol,
        price=price,
        quantity=quantity,
        buyer_id=buyer_id,
        seller_id=seller_id,
        buy_order_id=12345678,
        sell_order_id=87654321,
        timestamp=73,
    )


def test_buyer_side_decreases_cash_and_increases_position(portfolio):
    trade = make_trade(buyer_id=TRADER_ID, seller_id=5678, price=100.0, quantity=5)
    portfolio.process_trade(trade)
    assert portfolio.cash == INITIAL_CASH - 100.0 * 5
    assert portfolio.positions["AAPL"] == 5
    assert portfolio.trades == [trade]


def test_seller_side_increases_cash_and_goes_short(portfolio):
    trade = make_trade(buyer_id=5678, seller_id=TRADER_ID, price=100.0, quantity=5)
    portfolio.process_trade(trade)
    assert portfolio.cash == INITIAL_CASH + 100.0 * 5
    assert portfolio.positions["AAPL"] == -5   # short position
    assert portfolio.trades == [trade]


def test_unseen_symbol_does_not_raise(portfolio):
    trade = make_trade(buyer_id=TRADER_ID, seller_id=5678, symbol="NVDA")
    # Should not raise KeyError on a symbol never seen before.
    portfolio.process_trade(trade)
    assert portfolio.positions["NVDA"] == 5


def test_non_participating_trade_is_ignored(portfolio):
    trade = make_trade(buyer_id=4321, seller_id=5678)
    portfolio.process_trade(trade)   # trader is neither buyer nor seller
    assert portfolio.cash == INITIAL_CASH
    assert portfolio.positions == {}
    assert portfolio.trades == []


def test_get_realised_pnl(portfolio):
    trade = make_trade(buyer_id=5678, seller_id=TRADER_ID, price=100.0, quantity=5)
    portfolio.process_trade(trade)
    assert portfolio.get_realised_pnl() == portfolio.cash - INITIAL_CASH
    assert portfolio.get_realised_pnl() == 100.0 * 5
