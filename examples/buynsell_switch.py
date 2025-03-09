from core.strategy import Strategy

class BuyAndSellSwitch(Strategy):
    def on_bar(self) -> None:
        if self.position_size == 0:
            self.buy('AAPL', 1)
        else:
            self.sell('AAPL', 1)