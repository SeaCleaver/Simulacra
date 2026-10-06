# Tests for order_book.py: side routing, best price/order retrieval with
# price-time priority, spread/mid, empty-book None returns, filled-order removal,
# and add_order validation.

import pytest

from order import Order, BUY, SELL, LIMIT, MARKET
from order_book import OrderBook


@pytest.fixture
def book():
    return OrderBook("AAPL")


_next_id = [10000000]


def make_order(side, price, quantity=10, symbol="AAPL", order_type=LIMIT,
               trader_id=7223, timestamp=1):
    """Build a valid Order with a unique order_id each call."""
    _next_id[0] += 1
    return Order(_next_id[0], trader_id, symbol, side, order_type,
                 price, quantity, timestamp)


# --- construction ---

def test_lowercase_symbol_rejected():
    with pytest.raises(TypeError):
        OrderBook("aapl")


# --- side routing and best prices ---

def test_add_order_routes_to_correct_side(book):
    bid = make_order(BUY, 100.0)
    ask = make_order(SELL, 101.0)
    book.add_order(bid)
    book.add_order(ask)
    assert 100.0 in book.bids
    assert 101.0 in book.asks


def test_best_bid_and_ask_with_multiple_levels(book):
    book.add_order(make_order(BUY, 99.0))
    book.add_order(make_order(BUY, 100.0))
    book.add_order(make_order(SELL, 102.0))
    book.add_order(make_order(SELL, 101.0))
    assert book.get_best_bid() == 100.0   # highest bid
    assert book.get_best_ask() == 101.0   # lowest ask


# --- empty book None returns ---

def test_empty_book_returns_none(book):
    assert book.get_best_bid() is None
    assert book.get_best_ask() is None
    assert book.get_best_bid_order() is None
    assert book.get_best_ask_order() is None
    assert book.get_spread() is None
    assert book.get_mid_price() is None


# --- price-time priority ---

def test_best_bid_order_respects_time_priority(book):
    first = make_order(BUY, 100.0, timestamp=1)
    second = make_order(BUY, 100.0, timestamp=2)
    book.add_order(first)
    book.add_order(second)
    # Same price: the earliest (first added) sits at the front of the deque.
    assert book.get_best_bid_order() is first


def test_higher_priced_bid_becomes_best(book):
    low = make_order(BUY, 100.0)
    high = make_order(BUY, 101.0)
    book.add_order(low)
    book.add_order(high)
    assert book.get_best_bid() == 101.0
    assert book.get_best_bid_order() is high


# --- spread and mid ---

def test_spread_and_mid(book):
    book.add_order(make_order(BUY, 100.0))
    book.add_order(make_order(SELL, 101.0))
    assert book.get_spread() == 1.0
    assert book.get_mid_price() == 100.5


# --- filled-order removal ---

def test_remove_filled_order_cleans_best_level(book):
    order = make_order(SELL, 101.0, quantity=10)
    book.add_order(order)
    order.fill(10)
    book.remove_filled_order()
    # The best ask level was emptied and deleted.
    assert 101.0 not in book.asks
    assert book.get_best_ask() is None


def test_remove_filled_order_promotes_next_level(book):
    filled = make_order(SELL, 101.0, quantity=10)
    resting = make_order(SELL, 102.0, quantity=10)
    book.add_order(filled)
    book.add_order(resting)
    filled.fill(10)
    book.remove_filled_order()
    assert 101.0 not in book.asks
    assert book.get_best_ask() == 102.0
    assert book.get_best_ask_order() is resting


# --- add_order validation ---

def test_add_order_symbol_mismatch_rejected(book):
    other = make_order(BUY, 100.0, symbol="GOOG")
    with pytest.raises(ValueError):
        book.add_order(other)


def test_add_market_order_rejected(book):
    market = make_order(BUY, 0, order_type=MARKET)
    with pytest.raises(ValueError):
        book.add_order(market)


def test_add_filled_order_rejected(book):
    order = make_order(BUY, 100.0, quantity=10)
    order.fill(10)
    with pytest.raises(ValueError):
        book.add_order(order)
