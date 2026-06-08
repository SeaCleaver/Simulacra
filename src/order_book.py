# This file contains the class OrderBook for each ticker.
# The order book stores all active, unfilled limit orders.
# Bids are buy orders
# Best bid is the highest price buyers are asking for 
# Asks are sell orders
# Best ask is the lowest price sellers are asking for

from collections import deque
from order import Order, BUY, SELL, MARKET, LIMIT

class OrderBook:
    def __init__(self, symbol):
        self.symbol = symbol
    
        if not self.symbol.isupper():
            raise TypeError("All letters of a symbol must be uppercase.")
    
        # mapping is price -> dictionary of orders according to price levels
        self.bids = {}
        self.asks = {}
        
    def add_order(self, order: Order):
        
        # Validation
        if self.symbol != order.symbol:
            raise ValueError("Order's symbol does not match this book's.")
        
        if order.is_filled():
            raise ValueError("Order has already been filled.")
        
        if not order.is_limit():
            raise ValueError("Order needs to be a limit order.")
        
        if order.side is not BUY and order.side is not SELL:
            raise ValueError("Order can only have BUY or SELL sides.")
        
        
        # Execution
        # it is assumed that orders passed in are in chronological order
        if order.side == BUY:
            if order.price not in self.bids:
                self.bids[order.price] = deque()
                
            self.bids[order.price].append(order) 
            
        elif order.side == SELL:
            if order.price not in self.asks:
                self.asks[order.price] = deque()
                
            self.asks[order.price].append(order) 
        
    # gets the highest bid price
    def get_best_bid(self):
        if not self.bids:
            return None
        return max(self.bids)
    
    # gets the lowest ask price
    def get_best_ask(self):
        if not self.asks:
            return None
        return min(self.asks)
    
    # gets the earlaskt bid order at the highest price
    def get_best_bid_order(self):
        best_bid = self.get_best_bid()
        
        if best_bid == None:
            return None
        
        return self.bids[best_bid][0]
     
    # gets the earliest ask order at the lowest price
    def get_best_ask_order(self):
        best_ask = self.get_best_ask()
        
        if best_ask == None:
            return None
        
        return self.asks[best_ask][0]
    
    def remove_filled_order(self):
        self.remove_filled_bids()
        self.remove_filled_asks()
        
    # removing bids
    def remove_filled_bids(self):
        best_bid = self.get_best_bid()
        
        if best_bid is None:
            return
        
        while self.bids[best_bid] and self.bids[best_bid][0].is_filled():
            self.bids[best_bid].popleft()
            
        if not self.bids[best_bid]:
            del self.bids[best_bid]
           
    # removing asks
    def remove_filled_asks(self):
        best_ask = self.get_best_ask()
        
        if best_ask is None:
            return
        
        while self.asks[best_ask] and self.asks[best_ask][0].is_filled():
            self.asks[best_ask].popleft()
            
        if not self.asks[best_ask]:
            del self.asks[best_ask]
       
    # spread is the gap between the best bid and best ask
    # in a normal market, ask > bid 
    # so we use ask - bid     
    def get_spread(self):
        
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        if best_bid != None and best_ask != None:
            return round(best_ask - best_bid, 5)
        
        return None
    
    def get_mid_price(self):
        
        best_bid = self.get_best_bid()
        best_ask = self.get_best_ask()
        if best_bid != None and best_ask != None:
            return round((best_ask + best_bid) / 2, 5)
        
        return None
    
    # gets the total quantity of orders at each price level 
    # Not having =None will result in an error
    def get_report(self, levels=None):
        
        # array of tuples
        bid_report = []
        ask_report = []
        
        # bids: price -> deque of orders
        # price = key
        # orders = value (which is the deque of orders)
        for price, orders in self.bids.items():
            total_quantity = 0
            
            for order in orders:
                total_quantity += order.remaining_quantity
                
            bid_report.append((price, total_quantity)) 
            
            
        for price, orders in self.asks.items():
            total_quantity = 0
            
            for order in orders:
                total_quantity += order.remaining_quantity
                
            ask_report.append((price, total_quantity)) 
        
        # sort bids highest to lowest
        bid_report.sort(reverse=True)
        
        # sort asks lowest to highest
        ask_report.sort()
        
        # use slicing to cut out levels that aren't needed
        if levels != None:
            bid_report = bid_report[:levels]
            ask_report = ask_report[:levels]
        
        return {"bids": bid_report, "asks": ask_report}
    
# from pprint import pprint
    
# All test code shall be written below this line
# book1 = OrderBook('GOOG')
# order1 = Order(12345678, 7223, "GOOG", BUY, LIMIT, 300.14, 10, 12)
# order2 = Order(12345678, 7223, "GOOG", BUY, LIMIT, 300.13, 10, 13)
# order3 = Order(87654321, 7223, "GOOG", SELL, LIMIT, 300.15, 10, 12)
# book1.add_order(order1)
# book1.add_order(order2)
# book1.add_order(order3)
# print(book1.get_report())
# pprint(book1.bids)
# print(book1.get_best_ask())
# print(book1.get_best_ask_order())
# print(book1.get_spread())
# print(book1.get_mid_price())

# order1.fill(10)

# book1.remove_filled_order()
# print(book1.get_report())