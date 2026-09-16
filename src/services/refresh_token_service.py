from datetime import UTC, datetime, timedelta
from uuid import UUID

from src.core.security import (
    REFRESH_TOKEN_EXPIRATION_TIME_IN_DAYS,
    generate_refresh_token,
)
from src.repositories.refresh_token_repository import RefreshTokenRepository
from src.schemas.auth_schema import RefreshTokenCreate, RefreshTokenUpdate
from src.services.exceptions import (
    CompromisedSessionError,
    ExpiredRefreshTokenError,
    InvalidRefreshTokenError,
)


class RefreshTokenService:
    """Service layer for entity <RefreshToken>."""

    def __init__(self, repo: RefreshTokenRepository):
        self.repo = repo

    def create_token_for_user(self, user_id: UUID) -> str:
        token = generate_refresh_token()
        expires_at = (
            datetime.now(tz=UTC) + timedelta(days=REFRESH_TOKEN_EXPIRATION_TIME_IN_DAYS)
        ).replace(tzinfo=None)
        new_refresh_token_create_schema = RefreshTokenCreate(
            token=token, user_id=user_id, expires_at=expires_at, is_revoked=False
        )
        self.repo.create(new_refresh_token_create_schema)
        return token

    def validate_and_rotate_token(self, token: str) -> UUID:
        db_token = self.repo.get_by_token(token)
        if not db_token:
            raise InvalidRefreshTokenError("Token must be revoked.")
        if db_token.is_revoked:
            self.repo.revoke_all_user_tokens(db_token.user_id)
            raise CompromisedSessionError(user_id=db_token.user_id)
        if db_token.expires_at < datetime.now(tz=UTC).replace(tzinfo=None):
            raise ExpiredRefreshTokenError("Token must be revoked.")
        db_token_id = str(db_token.id)
        refresh_token_update_schema = RefreshTokenUpdate(is_revoked=True)
        self.repo.update(db_token_id, refresh_token_update_schema)
        return str(db_token.user_id)

    def revoke_token(self, token: str) -> None:
        db_token = self.repo.get_by_token(token)
        if not db_token:
            raise InvalidRefreshTokenError("Cannot be revoked.")
        db_token_id = db_token.id
        refresh_token_update_schema = RefreshTokenUpdate(is_revoked=True)
        self.repo.update(db_token_id, refresh_token_update_schema)
