from enum import Enum


class NotificationChannel(str, Enum):
    """Available channels for notification dispatching."""

    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"


class NotificationStatus(str, Enum):
    """Delivery lifecycle states of a single notification."""

    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
