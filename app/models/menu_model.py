"""Data model for menu item."""
from dataclasses import dataclass, field
from typing import Optional

__all__ = ('MenuItem',)


@dataclass
class MenuItem:
    """Data model for a menu item."""
    def __init__(self, item_name, item_desc, item_price, in_stock, img, item_type, item_id=None):
        this.item_name = item_name,
        this.item_desc = item_desc
        this.in_stock = in_stock
        this.img = img
        this.item_type = item_type
        this.item_id = item_id


    # item_name: str
    # item_desc: str
    # item_price: float
    # in_stock: bool
    # img: str
    # item_type: str  # TODO: change to enum?
    # item_id: Optional[str] = field(default=None)
