from fastapi import status

from src.models.refresh_token_model import RefreshToken


def test_login_returns_success_and_sets_secure_cookies(
    test_http_client, sample_single_user, sample_user_password
):
    """
    Tests POST /auth/login endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - validate JSON response.
    - response cookies includes access token and refresh token.
    """

    login_payload = {
        "email": sample_single_user.email,
        "password": sample_user_password,
    }

    response = test_http_client.post("/api/v1/auth/login", json=login_payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Successfully logged in."}

    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_login_returns_failure_when_credentials_are_invalid(
    test_http_client, sample_single_user
):
    """
    Tests POST /auth/login endpoint.
    Asserts:
    - response includes HTTP status code 401 when credentials are invalid.
    - response cookies don't include access token and refresh token.
    """

    login_payload = {"email": sample_single_user.email, "password": "ILoveWindows"}

    response = test_http_client.post("/api/v1/auth/login", json=login_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    assert "access_token" not in response.cookies
    assert "refresh_token" not in response.cookies


def test_refresh_session_returns_success_and_rotates_token(
    test_http_client, sample_single_user, sample_user_password, db_session
):
    """
    Tests POST /auth/refresh endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - validate JSON response.
    - response cookies includes access token and refresh token.
    - old refresh token exists in database.
    - old refresh token is revoked.
    """

    login_payload = {
        "email": sample_single_user.email,
        "password": sample_user_password,
    }

    login_response = test_http_client.post(
        "https://testserver/api/v1/auth/login", json=login_payload
    )
    old_refresh_token = login_response.cookies.get("refresh_token")

    refresh_response = test_http_client.post("https://testserver/api/v1/auth/refresh")

    assert refresh_response.status_code == status.HTTP_200_OK
    assert refresh_response.json() == {"message": "Token refreshed successfully."}

    assert "access_token" in refresh_response.cookies
    assert "refresh_token" in refresh_response.cookies

    db_refresh_token = (
        db_session.query(RefreshToken)
        .filter(RefreshToken.token == old_refresh_token)
        .first()
    )
    assert db_refresh_token is not None
    assert db_refresh_token.is_revoked == True


def test_refresh_session_returns_failure_when_cookies_are_missing(test_http_client):
    """
    Tests POST /auth/refresh endpoint.
    Asserts:
    - response includes HTTP status code 401 when access token and refresh token are missing from request cookies.
    """

    response = test_http_client.post("/api/v1/auth/refresh")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_clears_cookies_and_revokes_token(
    test_http_client, sample_single_user, sample_user_password, db_session
):
    """
    Tests POST /auth/logout endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response cookies don't include access token and refresh token.
    - old refresh token exists in the database.
    - old refresh token is revoked.
    """

    login_payload = {
        "email": sample_single_user.email,
        "password": sample_user_password,
    }
    login_response = test_http_client.post(
        "https://testserver/api/v1/auth/login", json=login_payload
    )
    active_refresh_token = login_response.cookies.get("refresh_token")

    logout_response = test_http_client.post("https://testserver/api/v1/auth/logout")

    assert logout_response.status_code == status.HTTP_200_OK
    assert logout_response.json() == {"message": "Logged out successfully."}

    assert "access_token" not in logout_response.cookies
    assert "refresh_token" not in logout_response.cookies

    db_refresh_token = (
        db_session.query(RefreshToken)
        .filter(RefreshToken.token == active_refresh_token)
        .first()
    )
    assert db_refresh_token is not None
    assert db_refresh_token.is_revoked == True
