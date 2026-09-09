# Matches BUY and SELL orders
# One engine per OrderBook

from order import Order
from trade import Trade
from order_book import OrderBook
import time

class MatchingEngine:
    def __init__(self, book: OrderBook):
        self.book = book 
        self.trades = [] # list of all trades executed
        self._next_trade_id = 1000000
        
    def match(self, incoming: Order):
        new_trades = []
        while not incoming.is_filled() and self._can_trade(incoming):
            if incoming.is_sell():
                resting: Order | None = self.book.get_best_bid_order()
            else: 
                resting: Order | None = self.book.get_best_ask_order()
                
            if resting is None: 
                break
                
            to_fill = min(incoming.remaining_quantity, 
                            resting.remaining_quantity)
            incoming.fill(to_fill)
            resting.fill(to_fill)
            trade = self._execute_trade(incoming, resting, to_fill)
            new_trades.append(trade)
            
            # if statement used here to avoid walking through deque on each use
            if resting.is_filled():
                self.book.remove_filled_order()
                
        if not incoming.is_filled():
            self.book.add_order(incoming)
            
        return new_trades
            
    # determines whether the incoming order can be matched with other orders in
    # the book
    def _can_trade(self, incoming: Order):
        if incoming.is_sell():
            price = self.book.get_best_bid()
            
            if price is None:
                return False
            elif incoming.price <= price:
                return True
            
        else:
            price = self.book.get_best_ask()
            
            if price is None:
                return False
            elif incoming.price >= price:
                return True
            
        return False
        
    # records the trade
    def _execute_trade(self, incoming: Order, resting: Order, quantity: int):
        timestamp = int(time.time())
        if incoming.is_buy():
            new = Trade(self._next_trade_id, self.book.symbol, resting.price, 
                        quantity, incoming.trader_id, resting.trader_id, 
                        incoming.order_id, resting.order_id, timestamp)
        else:
            new = Trade(self._next_trade_id, self.book.symbol, resting.price, 
                        quantity, resting.trader_id, incoming.trader_id, 
                        resting.order_id, incoming.order_id, timestamp)
            
        self._next_trade_id += 1
        self.trades.append(new)
        
        return new