# This file defines the Trade class.

from dataclasses import dataclass

@dataclass
class Trade:
    trade_id: int # seven digit
    symbol: str
    price: float
    quantity: int
    buyer_id: int # four digit
    seller_id: int # four digit
    buy_order_id: int # eight digit
    sell_order_id: int # eight digit
    timestamp: int
    
    def __post_init__(self):
        
        if self.trade_id < 1000000 or self.trade_id > 9999999:
            raise ValueError("Trade ID must be between "
                             "1000000 and 9999999 inclusive")
        
        if not self.symbol.isupper():
            raise ValueError("Company ticker/symbol must be all uppercase.")
        
        if (
            self.buy_order_id < 10000000 or self.buy_order_id > 99999999
            or self.sell_order_id < 10000000 or self.sell_order_id > 99999999
        ):
            raise ValueError("Order ID must be between " 
                            "10000000 and 99999999 inclusive.")
            
        if (
            self.buyer_id < 1000 or self.buyer_id > 9999
            or self.seller_id < 1000 or self.seller_id > 9999
        ):
            raise ValueError("Trader ID must be between " 
                             "1000 and 9999 inclusive.")
        
        if self.price <= 0:
            raise ValueError("Price cannot be negative.")
        
        if self.quantity <= 0:
            raise ValueError("Quantity cannot be lesser than 1.")
        
        if self.timestamp <= 0:
            raise ValueError("Timestamp must be positive.")
        
    def __str__(self):
        return (
            f"Trade {self.trade_id}: {self.buyer_id} ({self.buy_order_id}) and "
            f"{self.seller_id} ({self.sell_order_id}) traded {self.quantity} of"
            f" {self.symbol} @ {self.price} during {self.timestamp}"
        )
        
# Sample trade for testing purposes
new_trade = Trade(1234567, 'GOOG', 300.14, 5, 1234, 5678, 
                  12345678, 87654321, 73)

