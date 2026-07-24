from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.repositories.base_repository import BaseRepository
from src.models.user_model import User
from src.schemas.user_schema import UserCreate


class UserRepository(BaseRepository[User, UserCreate]):
    """Repository layer for entity <User>."""
    
    def __init__(self, db: Session):
        super().__init__(db, User)

    def create(self, new_user: UserCreate, hashed_password: str) -> User:
        new_user_data = new_user.model_dump()
        new_user_data.pop("password", None)
        user = User(**new_user_data, password_hash=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
