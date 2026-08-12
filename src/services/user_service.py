from uuid import UUID
from pwdlib import PasswordHash
from src.models.user_model import User
from src.schemas.user_schema import UserCreate
from src.repositories.user_repository import UserRepository
from src.services.exceptions import UserNotFoundError, UserInvalidPasswordError, UserEmailAlreadyExistsError, InvalidPaginationError


password_context = PasswordHash.recommended()


class UserService:
    "Service layer for entity <User>."

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_multi(self, *, offset: int = 0, limit: int = 100) -> list[User]:
        if offset < 0 or limit < 1 or limit > 100:
            raise InvalidPaginationError
        users = self.repo.get_multi(offset=offset, limit=limit)
        return users

    def get_by_id(self, user_id: UUID) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    def create(self, new_user: UserCreate) -> User:
        if len(new_user.password) < 6 or len(new_user.password) > 16:
            raise UserInvalidPasswordError("Password lenght must be >=6 and <= 16.")
        existing_user_with_same_email = self.repo.get_by_email(new_user.email)
        if existing_user_with_same_email:
            raise UserEmailAlreadyExistsError(new_user.email)
        hashed_password = password_context.hash(new_user.password)
        return self.repo.create(new_user, hashed_password=hashed_password)

    def delete(self, user_id: UUID) -> bool:
        user_exists = self.repo.delete(user_id)
        if not user_exists:
            raise UserNotFoundError(user_id)
        return user_exists
