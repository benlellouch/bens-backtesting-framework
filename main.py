import yfinance as yf

from core.engine import Engine
from examples.buynsell_switch import BuyAndSellSwitch


def main():
    data = yf.Ticker('AAPL').history(start='2022-12-01', end='2022-12-31', interval='1d')
    e = Engine(strategy=BuyAndSellSwitch(), ohlc_data=data)
    e.run()
    print(e._strategy.trades)


if __name__ == "__main__":
    main()
