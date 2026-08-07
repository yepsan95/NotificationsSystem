import logging
from typing import Generic, TypeVar, Sequence
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.base_model import Base


# Initialize logger for error logs
logger = logging.getLogger(__name__)

# Create generic types for BaseRepository class
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType]):
    """Base repository class. Will be inherited by all other repositories."""

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def _handle_exception(self, method_name: str, exception: Exception):
        if isinstance(exception, SQLAlchemyError):
            repo_name = self.__class__.__name__
            model_name = self.model.__name__
            logger.error(
                "[%s] Error in %s method, on %s: \n%s",
                repo_name,
                method_name,
                model_name,
                exception,
                exc_info=True
            )
            raise exception

    def get_by_id(self, id: UUID) -> ModelType | None:
        try:
            statement = select(self.model).where(self.model.id == id)
            return self.db.scalars(statement).first()
        except SQLAlchemyError as e:
            self._handle_exception("get_by_id", e)

    def get_multi(self, *, offset: int = 0, limit: int = 100) -> Sequence[ModelType]:
        try:
            statement = select(self.model).offset(offset).limit(limit)
            return self.db.scalars(statement).all()
        except SQLAlchemyError as e:
            self._handle_exception("get_multi", e)

    def create(self, new_obj: CreateSchemaType) -> ModelType:
        new_obj_data = new_obj.model_dump()
        db_obj = self.model(**new_obj_data)
        try:
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.db.rollback()
            self._handle_exception("create", e)

    def delete(self, id: UUID) -> bool:
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False
        try:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            self.handle_exception("delete", e)
