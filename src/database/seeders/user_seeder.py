from sqlalchemy.orm import Session

from src.database.factories.user_factory import UserFactory


def run_user_seeder(db: Session, count: int) -> None:
    if not isinstance(count, int):
        raise TypeError("Count must be a positive integer in the range 1 - 100.")
    if not 0 < count <= 100:
        raise ValueError(f""""
            Count must be in the range 1 - 100.
            Your input: {count}""")
    UserFactory._meta.sqlalchemy_session = db
    print(f"[SEEDER] Generating {count} users.")
    UserFactory.create_batch(count)
    print("[SEEDER] Users seed successful.")
    db.commit()
