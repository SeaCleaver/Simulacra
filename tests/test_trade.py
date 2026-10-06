# Tests for trade.py: __post_init__ validation constraints.

from typing import Any

import pytest

from trade import Trade


def make_trade(**overrides):
    """Build a valid Trade, overriding individual fields as needed."""
    kwargs: dict[str, Any] = dict(
        trade_id=1234567,
        symbol="GOOG",
        price=300.14,
        quantity=5,
        buyer_id=1234,
        seller_id=5678,
        buy_order_id=12345678,
        sell_order_id=87654321,
        timestamp=73,
    )
    kwargs.update(overrides)
    return Trade(**kwargs)


def test_valid_trade_constructs():
    trade = make_trade()
    assert trade.trade_id == 1234567


def test_trade_id_too_low_rejected():
    with pytest.raises(ValueError):
        make_trade(trade_id=999999)


def test_trade_id_too_high_rejected():
    with pytest.raises(ValueError):
        make_trade(trade_id=10000000)


def test_lowercase_symbol_rejected():
    with pytest.raises(ValueError):
        make_trade(symbol="goog")


def test_buy_order_id_out_of_range_rejected():
    with pytest.raises(ValueError):
        make_trade(buy_order_id=9999999)


def test_sell_order_id_out_of_range_rejected():
    with pytest.raises(ValueError):
        make_trade(sell_order_id=100000000)


def test_buyer_id_out_of_range_rejected():
    with pytest.raises(ValueError):
        make_trade(buyer_id=999)


def test_seller_id_out_of_range_rejected():
    with pytest.raises(ValueError):
        make_trade(seller_id=10000)


def test_non_positive_price_rejected():
    with pytest.raises(ValueError):
        make_trade(price=0)


def test_non_positive_quantity_rejected():
    with pytest.raises(ValueError):
        make_trade(quantity=0)


def test_non_positive_timestamp_rejected():
    with pytest.raises(ValueError):
        make_trade(timestamp=0)
