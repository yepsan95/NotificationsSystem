import logging

from src.core.notification_strategies.base_strategy import NotificationStrategy
from src.models.notification_model import Notification
from src.models.user_model import User

logger = logging.getLogger(__name__)


class PushNotificationStrategy(NotificationStrategy):
    """Strategy class for push notification dispatch."""

    def send(self, notification: Notification, user: User) -> bool:
        if not user.device_token:
            logger.error(
                "Push delivery failed: User with id '%s' has no active mobile device token registered.",
                user.id,
            )
            return False
        return True
