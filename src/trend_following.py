# A basic strategy that trades based on the trend
# buy when average trends up 
# sell when average trends down
# Lookback window determined by user

import numpy as np
from order import Order, BUY, SELL, LIMIT
from order_book import OrderBook
from strategy import Strategy

class TrendFollowingStrategy(Strategy):
    def __init__(self, trader_id, lookback, quantity, tick=0.01):
        self.trader_id = trader_id
        self.lookback = lookback
        self.quantity = quantity
        self.tick = tick
        self._next_order_id = 10000000
        
    def generate_order(self, book: OrderBook, price_history):
        mid = book.get_mid_price()
        if mid is None:
            return None

        # not enough data to compute average
        if len(price_history) < self.lookback:
            return None

        moving_average = np.mean(price_history[-self.lookback:])

        if mid > moving_average:
            side = BUY              
            price = mid + self.tick
        elif mid < moving_average:
            side = SELL             # price below average → trend down → sell
            price = mid - self.tick
        else:
            return None             # price exactly at average → do nothing

        order = Order(
            self._next_order_id, self.trader_id, book.symbol,
            side, LIMIT, round(price, 2), self.quantity,
            timestamp=len(price_history)
        )
        self._next_order_id += 1
        return order
        