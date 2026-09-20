from uuid import UUID

from pydantic import ValidationError

from src.core.notification_strategies.strategy_factory import (
    NotificationStrategyFactory,
)
from src.models.notification_enums import NotificationStatus
from src.models.notification_model import Notification
from src.repositories.notification_repository import NotificationRepository
from src.repositories.user_repository import UserRepository
from src.schemas.notification_schema import NotificationCreate, NotificationUpdate
from src.services.exceptions import (
    InvalidPaginationError,
    NotificationNotFoundError,
    UserNotFoundError,
)


class NotificationService:
    """Service layer for entity <Notification>."""

    def __init__(self, repo: NotificationRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo
        self.strategy_factory = NotificationStrategyFactory()

    def get_multi_by_user(
        self, user_id: UUID, *, offset: int = 0, limit: int = 100
    ) -> list[Notification]:
        if offset < 0 or limit < 1 or limit > 100:
            raise InvalidPaginationError()
        return self.repo.get_multi_by_user(user_id, offset=offset, limit=limit)

    def get_by_id_and_user(self, notification_id: UUID, user_id: UUID) -> Notification:
        notification = self.repo.get_by_id(notification_id)
        if not notification or str(notification.user_id) != user_id:
            raise NotificationNotFoundError(notification_id)
        return notification

    def create_and_send(
        self, user_id: UUID, new_notification: NotificationCreate
    ) -> Notification:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        db_notification = self.repo.create_with_owner(new_notification, user_id)
        strategy = self.strategy_factory.get_strategy(new_notification.channel)
        try:
            dispatch_success = strategy.send(db_notification, user)
            final_status = (
                NotificationStatus.SENT
                if dispatch_success
                else NotificationStatus.FAILED
            )
        except ValidationError:
            final_status = NotificationStatus.FAILED
        update_schema = NotificationUpdate(status=final_status)
        updated_notification = self.repo.update(str(db_notification.id), update_schema)
        return updated_notification

    def replace_by_user(
        self, notification_id: UUID, user_id: UUID, replace_schema: NotificationCreate
    ) -> Notification:
        notification = self.get_by_id_and_user(notification_id, user_id)
        if not notification:
            raise NotificationNotFoundError(notification_id)
        replaced_notification = self.repo.replace(notification_id, replace_schema)
        if not replaced_notification:
            raise NotificationNotFoundError(notification_id)
        return replaced_notification

    def update_by_user(
        self, notification_id: UUID, user_id: UUID, update_schema: NotificationUpdate
    ) -> Notification:
        notification = self.get_by_id_and_user(notification_id, user_id)
        if not notification:
            raise NotificationNotFoundError(notification_id)
        updated_notification = self.repo.update(notification_id, update_schema)
        if not updated_notification:
            raise NotificationNotFoundError(notification_id)
        return updated_notification

    def delete_by_user(self, notification_id: UUID, user_id: UUID) -> bool:
        self.get_by_id_and_user(notification_id, user_id)
        return self.repo.delete(notification_id)
