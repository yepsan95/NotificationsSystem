from fastapi import HTTPException, status

from src.core.notification_strategies.base_strategy import NotificationStrategy
from src.core.notification_strategies.email_strategy import EmailNotificationStrategy
from src.core.notification_strategies.push_strategy import PushNotificationStrategy
from src.core.notification_strategies.sms_strategy import SMSNotificationStrategy
from src.models.notification_enums import NotificationChannel


class NotificationStrategyFactory:
    def __init__(self):
        self._strategies: dict[NotificationChannel, NotificationStrategy] = {
            NotificationChannel.EMAIL: EmailNotificationStrategy(),
            NotificationChannel.SMS: SMSNotificationStrategy(),
            NotificationChannel.PUSH: PushNotificationStrategy(),
        }

    def get_strategy(self, channel: NotificationChannel) -> NotificationStrategy:
        strategy = self._strategies.get(channel)
        if not strategy:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Notification channel strategy from '{channel}' is not implemented.",
            )
        return strategy
