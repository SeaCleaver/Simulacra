# File containing the class for a trader's portfolio

from trade import Trade


class Portfolio:
    def __init__(self, trader_id: int, initial_cash: float):
        self.trader_id = trader_id
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.positions = {}
        self.trades = []
    
    def process_trade(self, trade: Trade):
        if self.trader_id == trade.buyer_id:
            self.cash -= trade.price * trade.quantity
            self.positions[trade.symbol] = (self.positions.get(trade.symbol, 0) 
                                            + trade.quantity)
            self.trades.append(trade)
            
        elif self.trader_id == trade.seller_id:
            self.cash += trade.price * trade.quantity
            self.positions[trade.symbol] = (self.positions.get(trade.symbol, 0) 
                                            - trade.quantity)
            self.trades.append(trade)
            
        else:
            raise ValueError("Trader ID given is not involved in the given "
                             "trade.")
    
    def get_realised_pnl(self):
        return self.cash - self.initial_cash
    