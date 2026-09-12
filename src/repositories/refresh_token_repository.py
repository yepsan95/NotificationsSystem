from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.models.refresh_token_model import RefreshToken
from src.repositories.base_repository import BaseRepository
from src.schemas.auth_schema import RefreshTokenCreate, RefreshTokenUpdate


class RefreshTokenRepository(BaseRepository[RefreshToken, RefreshTokenCreate, RefreshTokenUpdate]):
    """Repository layer for entity <RefreshToken>."""

    def __init__(self, db: Session):
        super().__init__(db, RefreshToken)

    def get_by_token(self, token: str) -> Optional[RefreshToken]:
        try:
            statement = select(RefreshToken).where(RefreshToken.token == token)
            return self.db.scalars(statement).first()
        except SQLAlchemyError as e:
            self._handle_exception("get_by_token", e)

    def revoke_all_user_tokens(self, user_id) -> None:
        try:
            update_obj = {"is_revoked": True}
            statement = (
                update(RefreshToken)
                .where(
                    RefreshToken.user_id == user_id,
                    RefreshToken.is_revoked == False
                )
                .values(update_obj)
                .returning(RefreshToken)
            )
            updated_refresh_token = self.db.scalars(statement).one()
            self.db.commit()
            self.db.refresh(updated_refresh_token)
            return updated_refresh_token
        except SQLAlchemyError as e:
            self.db.rollback()
            self._handle_exception("revoke_all_user_tokens", e)
