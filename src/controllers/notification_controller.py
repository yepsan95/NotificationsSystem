from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from src.controllers.dependencies import (
    CurrentUserDependency,
    DbDependency,
    PaginationDependency,
)
from src.repositories.notification_repository import NotificationRepository
from src.repositories.user_repository import UserRepository
from src.schemas.notification_schema import (
    NotificationCreate,
    NotificationResponse,
    NotificationUpdate,
)
from src.services.exceptions import (
    DatabaseConnectionError,
    InvalidPaginationError,
    NotificationNotFoundError,
)
from src.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/", response_model=list[NotificationResponse])
def get_user_notifications(
    pagination: PaginationDependency,
    db: DbDependency,
    current_user: CurrentUserDependency,
) -> list[NotificationResponse]:
    notification_repo = NotificationRepository(db)
    user_repo = UserRepository(db)
    notification_service = NotificationService(notification_repo, user_repo)
    try:
        return notification_service.get_multi_by_user(
            str(current_user.id), offset=pagination.offset, limit=pagination.limit
        )
    except InvalidPaginationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification_by_id(
    notification_id: UUID, db: DbDependency, current_user: CurrentUserDependency
) -> NotificationResponse:
    notification_repo = NotificationRepository(db)
    user_repo = UserRepository(db)
    notification_service = NotificationService(notification_repo, user_repo)
    try:
        return notification_service.get_by_id_and_user(
            notification_id, str(current_user.id)
        )
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED
)
def create_and_send_notification(
    new_notification: NotificationCreate,
    db: DbDependency,
    current_user: CurrentUserDependency,
) -> NotificationResponse:
    notification_repo = NotificationRepository(db)
    user_repo = UserRepository(db)
    notification_service = NotificationService(notification_repo, user_repo)
    try:
        return notification_service.create_and_send(
            str(current_user.id), new_notification
        )
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
)
def replace_notification(
    notification_id: UUID,
    replace_notification: NotificationCreate,
    db: DbDependency,
    current_user: CurrentUserDependency,
) -> NotificationResponse:
    notification_repo = NotificationRepository(db)
    user_repo = UserRepository(db)
    notification_service = NotificationService(notification_repo, user_repo)
    try:
        current_user_id = str(current_user.id)
        return notification_service.replace_by_user(
            notification_id, current_user_id, replace_notification
        )
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.patch(
    "/{notification_id}",
    response_model=NotificationResponse,
    status_code=status.HTTP_200_OK,
)
def update_notification(
    notification_id: UUID,
    update_notification: NotificationUpdate,
    db: DbDependency,
    current_user: CurrentUserDependency,
) -> NotificationResponse:
    notification_repo = NotificationRepository(db)
    user_repo = UserRepository(db)
    notification_service = NotificationService(notification_repo, user_repo)
    try:
        current_user_id = str(current_user.id)
        return notification_service.update_by_user(
            notification_id, current_user_id, update_notification
        )
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseConnectionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: UUID, db: DbDependency, current_user: CurrentUserDependency
) -> None:
    notification_repo = NotificationRepository(db)
    user_repo = UserRepository(db)
    notification_service = NotificationService(notification_repo, user_repo)
    try:
        notification_service.delete_by_user(notification_id, str(current_user.id))
    except NotificationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
