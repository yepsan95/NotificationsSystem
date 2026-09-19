from abc import ABC, abstractmethod

from src.models.notification_model import Notification
from src.models.user_model import User


class NotificationStrategy(ABC):
    """Abstract base notification strategy class. Will be inherited by all other notification strategies."""

    @abstractmethod
    def send(self, notification: Notification, user: User) -> bool:
        pass
