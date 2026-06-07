# This file defines the Order class.
# Dataclass makes the writing easier.

from dataclasses import dataclass
from enum import Enum

class Side(Enum):
    BUY = 1
    SELL = 2
    
class OrderType(Enum):
    LIMIT = 1
    MARKET = 2

BUY = Side.BUY
SELL = Side.SELL
LIMIT = OrderType.LIMIT
MARKET = OrderType.MARKET

@dataclass
class Order:
    order_id: int # eight digit
    trader_id: int # four digit
    symbol: str
    side: Side # BUY or SELL, to be changed to an enum later on
    order_type: Type # LIMIT or MARKET order, also to be changed to enum
    price: float
    quantity: int
    timestamp: int # follows the market data
    
    def __post_init__(self):
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        
        self.remaining_quantity = self.quantity
        
        if self.order_id < 10000000 or self.order_id > 99999999:
            raise ValueError("Order ID must be between " 
                             "10000000 and 99999999 inclusive.")
            
        if self.trader_id < 1000 or self.trader_id > 9999:
            raise ValueError("Trader ID must be between " 
                             "1000 and 9999 inclusive.")
            
        if not (self.side == BUY or self.side == SELL):
            raise ValueError("Orders can only be on the 'BUY' or 'SELL' side.")
        
        if not (self.order_type == LIMIT or 
                self.order_type == MARKET):
            raise ValueError("Order types can only be 'LIMIT' or 'MARKET'.")
        
        if self.order_type == LIMIT and not self.price:
            raise ValueError("Limit orders must have a price.")
        
        if self.order_type == LIMIT and self.price < 0:
            raise ValueError("Price must be positive.")
        
        if self.order_type == MARKET and self.price:
            raise ValueError("Market orders must not have a price. \n"
                             "Are you trying to place a Limit order instead?")
            
    def is_buy(self) -> bool:
        return (self.side == BUY)
    
    def is_sell(self) -> bool:
        return (self.side == SELL)
    
    def is_limit(self) -> bool:
        return (self.order_type == LIMIT)
    
    def is_market(self) -> bool:
        return (self.order_type == MARKET)
    
    def is_filled(self) -> bool:
        return (self.remaining_quantity == 0)
    
    def fill(self, amount) -> int:
        
        # immediately stops the program with the error message when triggered
        if amount <= 0:
            raise ValueError("Cannot be negative or zero.")
        
        if amount > self.remaining_quantity:
            raise ValueError("Amount cannot be higher than the "
                             "remaining quantity.")
        
        self.remaining_quantity -= amount
                
        return self.remaining_quantity
    
    def __str__(self):
        return (
            f"Order {self.order_id}: {self.side} "
            f"{self.remaining_quantity}/{self.quantity} "
            f"{self.symbol} @ {self.price}"
        )