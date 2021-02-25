"""Data model for an order."""
from dataclasses import dataclass
from datetime import datetime

__all__ = ('Order',)


@dataclass
class Order:
    """Data model for an order."""
    def __init__(self, order_id, order_subtotal, order_total, order_tax, customer_id, items_ordered, in_progress, order_date):
        this.order_id = order_id
        this.order_subtotal = order_subtotal
        this.order_total = order_total
        this.order_tax = order_tax
        this.customer_id = customer_id
        this.items_ordered = items_ordered
        this.in_progress = in_progress
        this.order_date = order_date

    # pylint: disable=too-many-instance-attributes

    # order_id: str
    # order_subtotal: float
    # order_total: float
    # order_tax: float
    # customer_id: str
    # items_ordered: list[str]  # a list of menu item IDs
    # in_progress: bool
    # order_date: datetime
