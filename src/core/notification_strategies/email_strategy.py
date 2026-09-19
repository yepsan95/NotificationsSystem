import logging

from pydantic import EmailStr, TypeAdapter, ValidationError

from src.core.notification_strategies.base_strategy import NotificationStrategy
from src.models.notification_model import Notification
from src.models.user_model import User

logger = logging.getLogger(__name__)


class EmailNotificationStrategy(NotificationStrategy):
    """Strategy class for Email notification dispatch."""

    def send(self, notification: Notification, user: User) -> bool:
        email_adapter = TypeAdapter(EmailStr)
        try:
            email_adapter.validate_python(user.email)
        except ValidationError as e:
            logger.error(
                "Email delivery failed: Invalid email address format: '%s'.\n%s",
                user.email,
                e,
            )
            return False
        return True
