from dataclasses import dataclass

from side import Side


@dataclass(frozen=True)
class Trade:
    """Created when an order is filled"""

    ticker: str
    side: Side
    price: float
    size: int
    index: int
    type: str
