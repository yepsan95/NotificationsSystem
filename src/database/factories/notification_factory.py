import random
import sys
from typing import ClassVar

import factory
from faker import Factory as FakerFactory
from sqlalchemy import String, cast, select

from src.models.notification_enums import NotificationChannel, NotificationStatus
from src.models.notification_model import Notification
from src.models.user_model import User

faker = FakerFactory.create()


class NotificationFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Notification
        sqlalchemy_session = None

    _channels_list: ClassVar[list[str]] = [
        channel.value for channel in NotificationChannel
    ]
    _statuses_list: ClassVar[list[str]] = [
        status.value for status in NotificationStatus
    ]
    _cached_user_ids: ClassVar[list[str] | None] = None

    title = factory.LazyAttribute(
        lambda _: generate_notification_template().get("title")
    )
    content = factory.LazyAttribute(
        lambda _: generate_notification_template().get("content")
    )
    channel = factory.LazyAttribute(
        lambda _: random.choice(NotificationFactory._channels_list)
    )
    status = factory.LazyAttribute(
        lambda _: random.choice(NotificationFactory._statuses_list)
    )
    user_id = factory.LazyAttribute(
        lambda _: random.choice(NotificationFactory._get_user_ids())
    )

    @classmethod
    def _get_user_ids(cls):
        """Queries all IDs from table users and saves them in cache memory."""

        if cls._cached_user_ids is not None:
            return cls._cached_user_ids
        session = cls._meta.sqlalchemy_session
        if session is None:
            raise RuntimeError("Missing SQLAlchemy session. Terminating process.")
        statement = select(cast(User.id, String))
        user_ids = session.scalars(statement).all()
        if not user_ids:
            print(
                "Table users is empty. At least one user must exist in order to generate notifications. Terminating process."
            )
            sys.exit(0)
        cls._cached_user_ids = user_ids
        return cls._cached_user_ids


def generate_notification_template():
    notification_templates = [
        {
            "title": f"Hello! Here's a new update: {faker.catch_phrase().title()}",
            "content": f"{faker.catch_phrase()}",
        },
        {
            "title": f"Message received! {faker.catch_phrase().title()}",
            "content": f"{faker.catch_phrase()}",
        },
        {
            "title": f"Friendly reminder: {faker.catch_phrase().title()}",
            "content": f"{faker.catch_phrase()}",
        },
        {
            "title": f"Don't forget! {faker.catch_phrase().title()}",
            "content": f"{faker.catch_phrase()}",
        },
        {
            "title": f"Breaking news! {faker.catch_phrase().title()}",
            "content": f"{faker.catch_phrase()}",
        },
    ]
    return random.choice(notification_templates)
