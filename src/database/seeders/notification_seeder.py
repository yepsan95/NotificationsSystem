from sqlalchemy.orm import Session

from src.database.factories.notification_factory import NotificationFactory


def run_notification_seeder(db: Session, count: int) -> None:
    if not isinstance(count, int):
        raise TypeError("Count must be a positive integer in the range 1 - 100.")
    if not 0 < count <= 100:
        raise ValueError(f"""
        Count must be in the range 1 - 100.
        Your input: {count}
        """)
    NotificationFactory._meta.sqlalchemy_session = db
    print(f"[SEEDER] Generating {count} notifications.")
    NotificationFactory.create_batch(count)
    print("[SEEDER] Notifications seed successful.")
    db.commit()
