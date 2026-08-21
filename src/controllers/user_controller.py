from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from src.services.user_service import UserService
from src.services.exceptions import UserNotFoundError, UserInvalidPasswordError, UserEmailAlreadyExistsError, InvalidPaginationError, DatabaseConnectionError
from src.repositories.user_repository import UserRepository
from src.schemas.user_schema import UserResponse, UserCreate, UserUpdate
from src.database.real_database import get_db
from src.controllers.dependencies import PaginationParams


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def get_multi_users(pagination: PaginationParams = Depends(),db: Session = Depends(get_db)) -> list[UserResponse]:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        return user_service.get_multi(offset=pagination.offset, limit=pagination.limit)
    except InvalidPaginationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service not available. Try again later."
        )


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)) -> UserResponse:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        return user_service.get_by_id(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(new_user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        return user_service.create(new_user)
    except UserInvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UserEmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def replace_user(user_id: UUID, replace_user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        return user_service.replace(user_id, replace_user)
    except UserInvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UserEmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: UUID, update_user: UserUpdate, db: Session = Depends(get_db)) -> UserResponse:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        return user_service.update(user_id, update_user)
    except UserInvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UserEmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)) -> None:
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    try:
        user_service.delete(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
