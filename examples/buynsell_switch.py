from core.strategy import Strategy


class BuyAndSellSwitch(Strategy):
    def on_bar(self):
        if self.position_size == 0:
            limit_price = self.close * 0.995
            self.buy_limit("AAPL", size=100, limit_price=limit_price)
            print(self._current_index, "buy")
        else:
            limit_price = self.close * 1.005
            self.sell_limit("AAPL", size=100, limit_price=limit_price)
            print(self._current_index, "sell")
