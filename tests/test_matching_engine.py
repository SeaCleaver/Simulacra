# Test file for testing how the matching engine handles different situations

from order_book import OrderBook
from matching_engine import MatchingEngine
from order import Order, BUY, SELL, LIMIT, MARKET
from trade import Trade

# orders that do not match rest in the book
def test_no_matching_orders():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    book.add_order(Order(10000001, 2001, "AAPL", SELL, LIMIT, 101.00, 10, 1)) 

    incoming = Order(10000002, 2002, "AAPL", BUY, LIMIT, 100.00, 10, 2)
    trades = engine.match(incoming)

    assert trades == []
    assert book.get_best_bid() == 100.00
    assert book.get_best_ask() == 101.00
    assert not incoming.is_filled()
    
# incoming order has same price as resting
def test_fill_matching_price_orders():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    book.add_order(Order(10000001, 2001, "AAPL", SELL, LIMIT, 100.00, 100, 1)) 

    incoming = Order(10000002, 2002, "AAPL", BUY, LIMIT, 100.00, 100, 2)
    trades = engine.match(incoming)
    
    assert trades == [Trade(trade_id=1000000, symbol='AAPL', price=100.0, 
                            quantity=100, buyer_id=2002, seller_id=2001, 
                            buy_order_id=10000002, sell_order_id=10000001, 
                            timestamp=2)]
    assert book.get_best_bid() == None
    assert book.get_best_ask() == None
    assert book.get_report() == {"bids": [], "asks": []}
    assert incoming.is_filled()
    
# incoming buy at high price fills ask at resting price
def test_high_buy_fills_at_resting_price():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    book.add_order(Order(10000001, 2001, "AAPL", SELL, LIMIT, 100.00, 10, 1)) 

    incoming = Order(10000002, 2002, "AAPL", BUY, LIMIT, 105.00, 10, 2)
    trades = engine.match(incoming)
    
    assert trades == [Trade(trade_id=1000000, symbol='AAPL', price=100.0, 
                            quantity=10, buyer_id=2002, seller_id=2001, 
                            buy_order_id=10000002, sell_order_id=10000001, 
                            timestamp=2)]
    assert incoming.is_filled()

# incoming sell at high price fills bid at resting price
def test_low_sell_fills_at_resting_price():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    book.add_order(Order(10000001, 2001, "AAPL", BUY, LIMIT, 100.00, 10, 1)) 

    incoming = Order(10000002, 2002, "AAPL", SELL, LIMIT, 99.00, 10, 2)
    trades = engine.match(incoming)
    
    assert trades == [Trade(trade_id=1000000, symbol='AAPL', price=100.0, 
                            quantity=10, buyer_id=2001, seller_id=2002,
                            buy_order_id=10000001, sell_order_id=10000002,
                            timestamp=2)]
    assert incoming.is_filled()

# incoming bid with lower quantity partially fills resting ask
def test_partially_fill_resting_order():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    book.add_order(Order(10000001, 2001, "AAPL", SELL, LIMIT, 100.00, 100, 1)) 

    incoming = Order(10000002, 2002, "AAPL", BUY, LIMIT, 100.00, 50, 2)
    trades = engine.match(incoming)
    
    assert trades == [Trade(trade_id=1000000, symbol='AAPL', price=100.0, 
                            quantity=50, buyer_id=2002, seller_id=2001, 
                            buy_order_id=10000002, sell_order_id=10000001, 
                            timestamp=2)]
    assert book.get_best_bid() == None
    assert incoming.is_filled()
    
    resting = book.get_best_ask_order()
    assert resting is not None
    assert resting.remaining_quantity == 50

# incoming bid with higher quantity gets partially filled
def test_incoming_order_partial_fill_then_rest():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    sell_order = Order(10000001, 2001, "AAPL", SELL, LIMIT, 100.00, 50, 1)
    book.add_order(sell_order) 

    incoming = Order(10000002, 2002, "AAPL", BUY, LIMIT, 100.00, 100, 2)
    trades = engine.match(incoming)
    
    assert trades == [Trade(trade_id=1000000, symbol='AAPL', price=100.0, 
                            quantity=50, buyer_id=2002, seller_id=2001, 
                            buy_order_id=10000002, sell_order_id=10000001, 
                            timestamp=2)]
    assert book.get_best_ask() == None
    assert sell_order.is_filled()
    
    resting = book.get_best_bid_order()
    assert resting is not None
    assert resting.remaining_quantity == 50

def test_fill_multiple_resting_orders():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    book.add_order(Order(10000001, 2001, "AAPL", SELL, LIMIT, 100.00, 50, 1))
    book.add_order(Order(10000002, 2001, "AAPL", SELL, LIMIT, 102.00, 50, 1))
    book.add_order(Order(10000003, 2001, "AAPL", SELL, LIMIT, 105.00, 50, 1))

    incoming = Order(10000004, 2002, "AAPL", BUY, LIMIT, 105.00, 120, 2)
    trades = engine.match(incoming)
    
    assert trades == [
        Trade(trade_id=1000000, symbol='AAPL', price=100.0, quantity=50, 
              buyer_id=2002, seller_id=2001, buy_order_id=10000004,
              sell_order_id=10000001, timestamp=2),
        Trade(trade_id=1000001, symbol='AAPL', price=102.0, quantity=50, 
              buyer_id=2002, seller_id=2001, buy_order_id=10000004,
              sell_order_id=10000002, timestamp=2),
        Trade(trade_id=1000002, symbol='AAPL', price=105.0, quantity=20, 
              buyer_id=2002, seller_id=2001, buy_order_id=10000004,
              sell_order_id=10000003, timestamp=2)
    ]
    
    assert book.get_best_bid() == None
    assert incoming.is_filled()
    
    resting = book.get_best_ask_order()
    assert resting is not None
    assert resting.remaining_quantity == 30
    
# the earlier order gets filled when there are two at the same price
def test_fill_earlier_order():
    book = OrderBook("AAPL")
    engine = MatchingEngine(book)
    early_order = Order(10000001, 2001, "AAPL", SELL, LIMIT, 100.00, 50, 1)
    later_order = Order(10000002, 2001, "AAPL", SELL, LIMIT, 100.00, 50, 2)
    book.add_order(early_order) 
    book.add_order(later_order)
    
    incoming = Order(10000003, 2002, "AAPL", BUY, LIMIT, 100.00, 50, 3)
    trades = engine.match(incoming)
    
    assert trades == [Trade(trade_id=1000000, symbol='AAPL', price=100.0, 
                        quantity=50, buyer_id=2002, seller_id=2001, 
                        buy_order_id=10000003, sell_order_id=10000001, 
                        timestamp=3)]
    assert early_order.is_filled()
    assert not later_order.is_filled()