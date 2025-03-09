from dataclasses import dataclass

from side import Side


@dataclass(frozen=True)
class Order:
    """Represents a buy or sell order"""

    ticker: str
    side: Side
    size: int
    index: int
    type: str = "market"
