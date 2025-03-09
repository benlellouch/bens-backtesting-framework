from dataclasses import dataclass

from core.side import Side


@dataclass(frozen=True)
class Trade:
    """Created when an order is filled"""

    ticker: str
    side: Side
    price: float
    size: int
    index: int
    type: str

    def __repr__(self) -> str:
        return f"<Trade: {self.index} {self.ticker} {self.size}@{self.price}>"
