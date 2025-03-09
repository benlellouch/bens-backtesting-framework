import pandas as pd
from tqdm import tqdm

from core.strategy import Strategy
from core.order import Order
from core.side import Side
from core.trade import Trade


class Engine:
    """The engine is the main object that will be use to run our backtesting"""

    def __init__(
        self,
        initial_cash: float = 100_000.0,
        strategy: Strategy = None,
        ohlc_data: pd.DataFrame = None,
    ) -> None:
        self._cash = initial_cash
        self._strategy = strategy
        self._data = ohlc_data
        self._current_index = None

    def set_stategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def set_data(self, ohlc_data: pd.DataFrame) -> None:
        self._data = ohlc_data

    def run(self) -> None:
        """Run given strategy on given data"""
        if self._strategy is None:
            raise AttributeError("Cannot run Engine without setting a strategy")
        if self._data is None:
            raise AttributeError("Cannot run a Strategy without data")

        self._strategy.data = self._data

        for idx in tqdm(self._data.index):
            self._current_index = self._strategy.current_idx = idx
            # fill orders from previous period
            self._fill_orders()

            # run strategy on current bar
            self._strategy.on_bar()

    def _fill_orders(self) -> None:
        """Fills buy and sell orders, creating new trade orders and adjusting cash balance"""
        for order in self._strategy.orders:
            if self._can_buy(order) or self._can_sell(order):
                trade = Trade(
                    ticker=order.ticker,
                    side=order.side,
                    price=self._data.loc[self._current_index]["Open"],
                    size=order.size,
                    type=order.type,
                    index=self._current_index,
                )

                self._strategy.add_trade(trade)
                self._cash -= trade.price * trade.size

    def _can_buy(self, order: Order):
        return (
            order.side == Side.BUY
            and self._cash >= self._data.loc[self._current_index]["Open"] * order.size
        )

    def _can_sell(self, order: Order):
        return order.side == Side.SELL and self._strategy.position_size >= order.size
