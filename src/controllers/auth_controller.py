from fastapi import APIRouter, HTTPException, Response, status

from src.controllers.dependencies import DbDependency, RefreshTokenDependency
from src.core.security import (
    ACCESS_TOKEN_EXPIRATION_TIME_IN_MINUTES,
    REFRESH_TOKEN_EXPIRATION_TIME_IN_DAYS,
    create_access_token,
    verify_password,
)
from src.repositories.refresh_token_repository import RefreshTokenRepository
from src.repositories.user_repository import UserRepository
from src.schemas.auth_schema import AuthMessageResponse, LoginRequest
from src.services.exceptions import (
    CompromisedSessionError,
    ExpiredRefreshTokenError,
    InvalidRefreshTokenError,
)
from src.services.refresh_token_service import RefreshTokenService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login", response_model=AuthMessageResponse, status_code=status.HTTP_200_OK
)
def login(
    login_data: LoginRequest, response: Response, db: DbDependency
) -> AuthMessageResponse:
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )
    refresh_token_repo = RefreshTokenRepository(db)
    refresh_token_service = RefreshTokenService(refresh_token_repo)
    access_token = create_access_token(subject=str(user.id))
    refresh_token = refresh_token_service.create_token_for_user(user_id=str(user.id))
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRATION_TIME_IN_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRATION_TIME_IN_DAYS * 24 * 60 * 60,
    )
    return AuthMessageResponse(message="Successfully logged in.")


@router.post(
    "/refresh", response_model=AuthMessageResponse, status_code=status.HTTP_200_OK
)
def refresh_session(
    response: Response, refresh_token: RefreshTokenDependency, db: DbDependency
) -> AuthMessageResponse:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing."
        )
    refresh_token_repo = RefreshTokenRepository(db)
    refresh_token_service = RefreshTokenService(refresh_token_repo)

    try:
        user_id = refresh_token_service.validate_and_rotate_token(refresh_token)
        new_access_token = create_access_token(subject=user_id)
        new_refresh_token = refresh_token_service.create_token_for_user(user_id=user_id)
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRATION_TIME_IN_MINUTES * 60,
        )
        response.set_cookie(
            key="refresh_token",
            value=new_refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=REFRESH_TOKEN_EXPIRATION_TIME_IN_DAYS * 24 * 60 * 60,
        )
        return AuthMessageResponse(message="Token refreshed successfully.")
    except InvalidRefreshTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except ExpiredRefreshTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except CompromisedSessionError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post(
    "/logout", response_model=AuthMessageResponse, status_code=status.HTTP_200_OK
)
def logout(
    response: Response, refresh_token: RefreshTokenDependency, db: DbDependency
) -> AuthMessageResponse:
    if refresh_token:
        refresh_token_repo = RefreshTokenRepository(db)
        refresh_token_service = RefreshTokenService(refresh_token_repo)
        refresh_token_service.revoke_token(refresh_token)
    response.delete_cookie(
        key="access_token", secure=True, httponly=True, samesite="lax"
    )
    response.delete_cookie(
        key="refresh_token", secure=True, httponly=True, samesite="lax"
    )
    return AuthMessageResponse(message="Logged out successfully.")
