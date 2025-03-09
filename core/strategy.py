from typing import List

from core.order import Order
from core.side import Side
from core.trade import Trade


class Strategy:
    """Handles the execution logic of strategy"""

    def __init__(self) -> None:
        self._current_idx = None
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

    def add_trade(self, trade: Trade) -> None:
        self._trades.append(trade)

    def buy(self, ticker: str, size=1) -> None:
        self._orders.append(
            Order(ticker=ticker, side=Side.BUY, size=size, index=self._current_idx)
        )

    def sell(self, ticker: str, size=1) -> None:
        self._orders.append(
            Order(ticker=ticker, side=Side.SELL, size=-size, index=self._current_idx)
        )

    def on_bar(self) -> None:
        """To be implemented by strategy"""
        raise NotImplementedError
