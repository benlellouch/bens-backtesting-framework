from typing import List

from core.order import Order
from core.side import Side
from core.trade import Trade
from core.consts import CLOSE, OPEN, HIGH, LOW, LIMIT

class Strategy:
    """Handles the execution logic of strategy"""

    def __init__(self) -> None:
        self._current_index = None
        self._data = None
        self._orders = []
        self._trades = []

    @property
    def orders(self) -> List[Order]:
        return self._orders

    @property
    def position_size(self) -> int:
        return sum(t.size for t in self._trades)
    
    @property
    def trades(self):
        return self._trades

    @property
    def close(self):
        return self._data.loc[self._current_index][CLOSE]
    
    @property
    def open(self):
        return self._data.loc[self._current_index][OPEN]

    @property
    def high(self):
        return self._data.loc[self._current_index][HIGH]
    
    @property
    def low(self):
        return self._data.loc[self._current_index][LOW]

    def add_trade(self, trade: Trade) -> None:
        self._trades.append(trade)

    def buy(self, ticker: str, size: int=1) -> None:
        self._orders.append(
            Order(ticker=ticker, side=Side.BUY, size=size, index=self._current_index)
        )
    
    def buy_limit(self, ticker:str, limit_price:float, size: int=1) -> None:
        self.orders.append(
            Order(ticker=ticker, side=Side.BUY, size=size, limit_price=limit_price, type=LIMIT, index=self._current_index)
        )

    def sell(self, ticker: str, size=1) -> None:
        self._orders.append(
            Order(ticker=ticker, side=Side.SELL, size=-size, index=self._current_index)
        )
    

    def sell_limit(self, ticker:str, limit_price:float, size: int=1) -> None:
        self.orders.append(
            Order(ticker=ticker, side=Side.SELL, size=-size, limit_price=limit_price, type=LIMIT, index=self._current_index)
        )


    def on_bar(self) -> None:
        """To be implemented by strategy"""
        raise NotImplementedError
