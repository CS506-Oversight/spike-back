"""Data model for an user."""
from dataclasses import dataclass

__all__ = ('User',)


@dataclass
class User:
    """User data model."""
    def __init__(self, user_id, username, password, phone, address, email, type="staff"):
        this.user_id = user_id
        this.username = username
        this.password = password
        this.phone = phone
        this.address = address
        this.email = email
        this.type = type

    # user_id: str
    # username: str
    # password: str
    # phone: str
    # address: str
    # email: str
    # type: str  # TODO: change to enum?
