from order import Order
from side import Side


class Strategy:
    """Handles the execution logic of strategy"""

    def __init__(self) -> None:
        self._current_idx = None
        self._data = None
        self._orders = []
        self._trades = []

    def buy(self, ticker: str, size=1) -> None:
        self._orders.append(
            Order(ticker=ticker, side=Side.BUY, size=size, index=self._current_idx)
        )

    def sell(self, ticker: str, size=1) -> None:
        self._orders.append(
            Order(ticker=ticker, side=Side.SELL, size=-size, index=self._current_idx)
        )

    @property
    def position_size(self) -> int:
        return sum(t.size for t in self._trades)

    def on_bar(self) -> None:
        """To be implemented by strategy"""
        raise NotImplementedError
