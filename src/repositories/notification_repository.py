from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.notification_model import Notification
from src.repositories.base_repository import BaseRepository
from src.schemas.notification_schema import NotificationCreate, NotificationUpdate


class NotificationRepository(
    BaseRepository[Notification, NotificationCreate, NotificationUpdate]
):
    """Repository layer for entity <Notification>."""

    def __init__(self, db: Session):
        super().__init__(db, Notification)

    def get_multi_by_user(
        self, user_id: UUID, *, offset: int = 0, limit: int = 100
    ) -> Sequence[Notification]:
        try:
            statement = (
                select(Notification)
                .where(Notification.user_id == user_id)
                .offset(offset)
                .limit(limit)
            )
            return self.db.scalars(statement).all()
        except SQLAlchemyError as e:
            self._handle_exception("get_multi_by_user", e)

    def create_with_owner(
        self, new_notification: NotificationCreate, user_id: UUID
    ) -> Notification:
        new_notification_data = new_notification.model_dump()
        new_notification_data["user_id"] = user_id
        db_notification = Notification(**new_notification_data)
        try:
            self.db.add(db_notification)
            self.db.commit()
            self.db.refresh(db_notification)
            return db_notification
        except SQLAlchemyError as e:
            self.db.rollback()
            self._handle_exception("create_with_owner", e)
