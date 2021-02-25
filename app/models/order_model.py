"""Data model for an order."""
from dataclasses import dataclass
from datetime import datetime

__all__ = ('Order',)


@dataclass
class Order:
    """Data model for an order."""

    order_id: str
    order_subtotal: float
    order_total: float
    order_tax: float
    customer_id: str
    items_ordered: list[str]  # a list of menu item IDs
    in_progress: bool
    order_date: datetime
