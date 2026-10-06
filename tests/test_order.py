# Tests for order.py: __post_init__ validation and the fill() lifecycle.

from typing import Any

import pytest

from order import Order, BUY, SELL, LIMIT, MARKET


def make_order(**overrides):
    """Build a valid limit Order, overriding individual fields as needed."""
    kwargs: dict[str, Any] = dict(
        order_id=12345678,
        trader_id=7223,
        symbol="AAPL",
        side=BUY,
        order_type=LIMIT,
        price=300.14,
        quantity=10,
        timestamp=12,
    )
    kwargs.update(overrides)
    return Order(**kwargs)


# --- construction of valid orders ---

def test_valid_limit_order_constructs():
    order = make_order()
    assert order.remaining_quantity == 10


def test_valid_market_order_constructs():
    # Market orders must have a falsy price (0).
    order = make_order(order_type=MARKET, price=0)
    assert order.remaining_quantity == 10


# --- validation rejections ---

def test_order_id_too_low_rejected():
    with pytest.raises(ValueError):
        make_order(order_id=9999999)


def test_order_id_too_high_rejected():
    with pytest.raises(ValueError):
        make_order(order_id=100000000)


def test_trader_id_too_low_rejected():
    with pytest.raises(ValueError):
        make_order(trader_id=999)


def test_trader_id_too_high_rejected():
    with pytest.raises(ValueError):
        make_order(trader_id=10000)


def test_lowercase_symbol_rejected():
    with pytest.raises(ValueError):
        make_order(symbol="aapl")


def test_market_order_with_price_rejected():
    with pytest.raises(ValueError):
        make_order(order_type=MARKET, price=300.14)


def test_limit_order_without_price_rejected():
    with pytest.raises(ValueError):
        make_order(price=0)


def test_non_positive_quantity_rejected():
    with pytest.raises(ValueError):
        make_order(quantity=0)


def test_non_positive_timestamp_rejected():
    with pytest.raises(ValueError):
        make_order(timestamp=0)


# --- fill() and is_filled() ---

def test_fill_reduces_remaining_quantity():
    order = make_order(quantity=10)
    remaining = order.fill(4)
    assert remaining == 6
    assert order.remaining_quantity == 6


def test_full_fill_flips_is_filled():
    order = make_order(quantity=10)
    assert not order.is_filled()
    order.fill(10)
    assert order.is_filled()


def test_overfill_rejected():
    order = make_order(quantity=10)
    with pytest.raises(ValueError):
        order.fill(11)


def test_fill_non_positive_amount_rejected():
    order = make_order(quantity=10)
    with pytest.raises(ValueError):
        order.fill(0)
    with pytest.raises(ValueError):
        order.fill(-3)
