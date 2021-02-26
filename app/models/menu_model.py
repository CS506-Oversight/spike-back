"""Data model for menu item."""
from dataclasses import dataclass, field
from typing import Optional

__all__ = ('MenuItem',)


@dataclass
class MenuItem:
    """Data model for a menu item."""

    item_name: str
    item_desc: str
    item_price: float
    in_stock: bool
    img: str
    item_type: str  # TODO: change to enum?
    item_id: Optional[str] = field(default=None)
