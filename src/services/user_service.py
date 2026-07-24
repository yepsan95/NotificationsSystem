from uuid import UUID
from pwdlib import PasswordHash
from src.models.user_model import User
from src.schemas.user_schema import UserCreate
from src.repositories.user_repository import UserRepository


password_context = PasswordHash.recommended()


class UserService:
    "Service layer for entity <User>."

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_all(self) -> list[User]:
        users = self.repo.get_all()
        return users

    def get_by_id(self, user_id: UUID) -> User:
        user = self.repo.get_by_id(user_id)
        return user

    def create(self, new_user: UserCreate) -> User:
        hashed_password = password_context.hash(new_user.password)
        return self.repo.create(new_user, hashed_password=hashed_password)

    def delete(self, user_id: UUID) -> bool:
        return self.repo.delete(user_id)
