"""Data model for an order."""
from dataclasses import dataclass
from datetime import datetime

__all__ = ('Order',)


@dataclass
class Order:
    """Data model for an order."""

    order_id: str
    order_subtotal: float
    order_tax: float
    customer_name: str
    customer_email: str
    items_ordered: list[str]  # a list of menu item IDs
    order_date: datetime  # TODO: Check if this needs some transformation to store it in the db or not
