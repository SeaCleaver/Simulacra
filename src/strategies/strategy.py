# holds the strategy class. 
# any future strategies should build from this class.

from abc import abstractmethod
from order import Order
from order_book import OrderBook

class Strategy:
    @abstractmethod
    def generate_order(self, book: OrderBook, price_history: list) -> Order | None:
        pass