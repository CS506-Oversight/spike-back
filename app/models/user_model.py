"""Data model for an user."""
from dataclasses import dataclass

__all__ = ('User',)


@dataclass
class User:
    """User data model."""

    username: str
    password: str
    phone: str
    address: str
    email: str
    type: str  # TODO: change to enum?
