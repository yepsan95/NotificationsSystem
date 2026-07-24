from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserResponse, UserCreate
from src.database.database import get_db


router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)) -> list[UserResponse]:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_all()

@router.get("/{id}", response_model=UserResponse)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)) -> UserResponse:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.get_by_id(user_id)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    return user_service.create(new_user)

