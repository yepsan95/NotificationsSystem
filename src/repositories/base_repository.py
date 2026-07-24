from typing import Generic, TypeVar, Sequence
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.base_model import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType]):
    """Base repository class. Will be inherited by all other repositories."""

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def get_by_id(self, id: UUID) -> ModelType | None:
        statement = select(self.model).where(self.model.id == id)
        return self.db.scalars(statement).first()
    
    def get_all(self) -> Sequence[ModelType]:
        statement = select(self.model)
        return self.db.scalars(statement).all()

    def create(self, new_obj: CreateSchemaType) -> ModelType:
        new_obj_data = new_obj.mode_dump()
        db_obj = self.model(**new_obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: UUID) -> bool:
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
