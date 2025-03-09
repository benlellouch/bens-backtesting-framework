import pandas as pd
from tqdm import tqdm
from strategy import Strategy


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
            print(idx)

    def _fill_orders(self) -> None:
        """Fills orders from previous period"""
        pass
