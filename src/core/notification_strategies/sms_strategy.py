import logging

from src.core.notification_strategies.base_strategy import NotificationStrategy
from src.models.notification_model import Notification
from src.models.user_model import User

logger = logging.getLogger(__name__)


class SMSNotificationStrategy(NotificationStrategy):
    """Strategy class for SMS notification dispatch."""

    def send(self, notification: Notification, user: User) -> bool:
        if not user.phone_number:
            logger.error(
                "SMS delivery failed: User with id '%s' does not have a registered phone number.",
                user.id,
            )
            return False
        if len(notification.content) > 160:
            logger.error(
                "SMS delivery failed: Content exceeds the 160 characters limit. Lenght: %s characters.",
                len(notification.content),
            )
            return False
        return True
