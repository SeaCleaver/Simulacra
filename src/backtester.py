# Backtester class that accesses the order_book, matching engine, and portfolio.
# Built for mean reversion strategy, but other strategies can be used.

from matching_engine import MatchingEngine
from portfolio import Portfolio
from strategy import Strategy
from order import Order

class Backtester:
    def __init__(self, engine: MatchingEngine, portfolio: Portfolio, 
                 strategy: Strategy):
        self.engine = engine
        self.portfolio = portfolio
        self.strategy = strategy
        self.price_history = []
        self.pnl_history = []
        
    # main method for running everything
    def run(self, events: list[Order]):
        for event in events:
            # updating price history
            mid = self.engine.book.get_mid_price()
            if mid is not None:
                self.price_history.append(mid)
            
            # get action from strategy
            order = self.strategy.generate_order(self.engine.book, 
                                                 self.price_history)
            
            # match a new order if not null
            if order:
                new_trades = self.engine.match(order)
                for trade in new_trades:
                    self.portfolio.process_trade(trade)
            
            # update next market event
            market_trades = self.engine.match(event)
            for trade in market_trades:
                self.portfolio.process_trade(trade)
                
            self.pnl_history.append(self.portfolio.get_realised_pnl())
                
    
    # retrieve results from the portfolio
    def get_results(self):
        return {
            "pnl": self.portfolio.get_realised_pnl(),
            "trades": self.portfolio.trades,
            "positions": self.portfolio.positions
        }