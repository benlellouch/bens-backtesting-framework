from typing import Tuple

import numpy as np
import pandas as pd
from tqdm import tqdm

from core.strategy import Strategy
from core.order import Order
from core.side import Side
from core.trade import Trade
from core.consts import HIGH, LOW, OPEN, CLOSE, LIMIT


class Engine:
    """The engine is the main object that will be use to run our backtesting"""

    def __init__(
        self,
        initial_cash: float = 100_000.0,
        strategy: Strategy = None,
        ohlc_data: pd.DataFrame = None,
    ) -> None:
        self._risk_free_rate = 0
        self._trading_days = 252
        self._initial_cash = self._cash = initial_cash
        self._strategy = strategy
        self._data = ohlc_data
        self._current_index = None
        self._cash_series = {}
        self._stock_series = {}

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

        self._strategy._data = self._data

        for idx in tqdm(self._data.index):
            self._current_index = self._strategy._current_index = idx
            # fill orders from previous period
            self._fill_orders()

            # run strategy on current bar
            self._strategy.on_bar()

            self._cash_series[idx] = self._cash
            self._stock_series[idx] = (
                self._strategy.position_size
                * self._data.loc[self._current_index][CLOSE]
            )

    def _fill_orders(self) -> None:
        """Fills buy and sell orders, creating new trade orders and adjusting cash balance"""
        for order in self._strategy.orders:
            can_fill, fill_price = self._determine_fill_price(order)
            if can_fill:
                trade = Trade(
                    ticker=order.ticker,
                    side=order.side,
                    price=fill_price,
                    size=order.size,
                    type=order.type,
                    index=self._current_index,
                )

                self._strategy.add_trade(trade)
                self._cash -= trade.price * trade.size

    def _determine_fill_price(self, order: Order) -> Tuple[bool, float]:
        fill_price = self._data.loc[self._current_index][OPEN]
        can_fill = False
        if self._can_buy(order):
            can_fill = True
            if order.type == LIMIT:
                if order.limit_price >= self._data.loc[self._current_index][LOW]:
                    fill_price = order.limit_price
                    print(
                        self._current_index,
                        "Buy Filled. ",
                        "limit",
                        order.limit_price,
                        " / low",
                        self._data.loc[self._current_index]["Low"],
                    )
                else:
                    can_fill = False
                    print(
                        self._current_index,
                        "Buy NOT filled. ",
                        "limit",
                        order.limit_price,
                        " / low",
                        self._data.loc[self._current_index]["Low"],
                    )
        if self._can_sell(order):
            can_fill = True
            if order.type == LIMIT:
                if order.limit_price <= self._data.loc[self._current_index][HIGH]:
                    fill_price = order.limit_price
                    print(
                        self._current_index,
                        "Sell filled. ",
                        "limit",
                        order.limit_price,
                        " / high",
                        self._data.loc[self._current_index]["High"],
                    )
                else:
                    print(
                        self._current_index,
                        "Sell NOT filled. ",
                        "limit",
                        order.limit_price,
                        " / high",
                        self._data.loc[self._current_index]["High"],
                    )

        return can_fill, fill_price

    def _can_buy(self, order: Order):
        return (
            order.side == Side.BUY
            and self._cash >= self._data.loc[self._current_index][OPEN] * order.size
        )

    def _can_sell(self, order: Order):
        return order.side == Side.SELL and self._strategy.position_size >= order.size

    def _get_max_drawdown(self, close: pd.Series) -> float:
        roll_max = close.cummax()
        daily_drawdown = close / roll_max - 1.0
        return daily_drawdown.min() * 100

    def _get_stats(self):
        metrics = {}
        portfolio = pd.DataFrame(
            {"stock": self._stock_series, "cash": self._cash_series}
        )
        portfolio["total_aum"] = portfolio["stock"] + portfolio["cash"]
        aum = portfolio["total_aum"]
        portfolio_bh = (
            self._initial_cash
            / self._data.loc[self._data.index[0]][OPEN]
            * self._data.Close
        )

        total_return = 100 * (
            (
                self._data.loc[self._current_index][CLOSE]
                * self._strategy.position_size
                + self._cash
            )
            / self._initial_cash
            - 1
        )

        metrics["total_return"] = total_return
        metrics["exposure_pct"] = (
            (portfolio["stock"] / portfolio["total_aum"]) * 100
        ).mean()
        metrics["returns_annualized"] = (
            (aum.iloc[-1] / aum.iloc[0])
            ** (1 / ((aum.index[-1] - aum.index[0]).days / 365))
            - 1
        ) * 100
        metrics["returns_bh_annualized"] = (
            (portfolio_bh.iloc[-1] / portfolio_bh.iloc[0])
            ** (1 / ((portfolio_bh.index[-1] - portfolio_bh.index[0]).days / 365))
            - 1
        ) * 100
        metrics["volatility_ann"] = (
            aum.pct_change().std() * np.sqrt(self._trading_days) * 100
        )
        metrics["volatility_bh_ann"] = (
            portfolio_bh.pct_change().std() * np.sqrt(self._trading_days) * 100
        )
        metrics["sharpe_ratio"] = (
            metrics["returns_annualized"] - self._risk_free_rate
        ) / metrics["volatility_ann"]
        metrics["sharpe_ratio_bh"] = (
            metrics["returns_bh_annualized"] - self._risk_free_rate
        ) / metrics["volatility_bh_ann"]
        metrics["max_drawdown"] = self._get_max_drawdown(self._data.Close)
        return metrics
