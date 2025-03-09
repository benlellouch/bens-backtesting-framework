import yfinance as yf
from core.engine import Engine
from core.strategy import Strategy


def main():
    data = yf.Ticker("AAPL").history(
        start="2020-01-01", end="2022-12-31", interval="1d"
    )
    e = Engine(strategy=Strategy(), ohlc_data=data)
    e.run()


if __name__ == "__main__":
    main()
