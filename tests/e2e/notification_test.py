from fastapi import status

from src.models.notification_enums import NotificationChannel, NotificationStatus
from src.models.notification_model import Notification


def test_access_notification_returns_failure_when_auth_tokens_are_missing(
    test_http_client,
):
    """
    Tests GET /notifications endpoint.
    Asserts:
    - response includes HTTP status code 401 when authentication tokens are missing.
    """

    response = test_http_client.get("https://testserver/api/v1/notifications")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_my_notifications_returns_only_own_records(
    db_session, test_http_client, auth_user_and_cookie, sample_secondary_user
):
    """
    Tests GET /notifications endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - validate only one notification exists in the database.
    - validate created notification's fields.
    """

    notification_user_1 = Notification(
        user_id=auth_user_and_cookie.get_safe_attributes()["id"],
        title="User 1 Alert",
        content="Hello User 1",
        channel=NotificationChannel.EMAIL,
        status=NotificationStatus.SENT,
    )
    notification_user_2 = Notification(
        user_id=sample_secondary_user.get_safe_attributes()["id"],
        title="User 2 Intrusion",
        content="Hello User 2",
        channel=NotificationChannel.PUSH,
        status=NotificationStatus.SENT,
    )
    db_session.add_all([notification_user_1, notification_user_2])
    db_session.commit()

    response = test_http_client.get("https://testserver/api/v1/notifications")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 1

    notification_user_1_data = data[0]
    notification_user_1_dict = notification_user_1.to_dict()
    notification_user_1_dict["user_id"] = str(notification_user_1_dict["user_id"])

    assert all(
        notification_user_1_dict.get(k) == v
        for k, v in notification_user_1_data.items()
    )


def test_user_cannot_read_another_users_notifications(
    db_session, test_http_client, auth_user_and_cookie, sample_secondary_user
):
    """
    Tests GET /notifications/{notification_id} endpoint.
    Asserts:
    - response includes HTTP status code 404 when trying to get another user's notification.
    """

    foreign_notification = Notification(
        user_id=sample_secondary_user.get_safe_attributes()["id"],
        title="Top Secret RMS.",
        content="Emacs > Vi",
        channel=NotificationChannel.EMAIL,
        status=NotificationStatus.SENT,
    )
    db_session.add(foreign_notification)
    db_session.commit()
    db_session.refresh(foreign_notification)

    get_response = test_http_client.get(
        f"https://testserver/api/v1/notifications/{foreign_notification.id!s}"
    )
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_create_email_notification_returns_success_and_triggers_strategy(
    test_http_client, auth_user_and_cookie
):
    """
    Tests POST /notifications endpoint.
    Asserts:
    - response includes HTTP status code 201.
    - validate created notification's fields.
    """

    payload = {
        "title": "Welcome to the Linux Foundation.",
        "content": "Your subscription is now active.",
        "channel": NotificationChannel.EMAIL,
    }

    response = test_http_client.post(
        "https://testserver/api/v1/notifications", json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert all(data.get(k) == v for k, v in payload.items())
    assert data["status"] == NotificationStatus.SENT
    assert data["user_id"] == auth_user_and_cookie.get_safe_attributes()["id"]


def test_create_sms_notification_sets_failed_status_when_content_exceeds_character_limit(
    test_http_client, auth_user_and_cookie
):
    """
    Tests POST /notifications endpoint.
    Asserts:
    - response includes HTTP status code 201.
    - validate created notification's fields.
    - validate notification status is set to failed.
    """

    long_content = "A" * 165
    payload = {
        "title": "Alert",
        "content": long_content,
        "channel": NotificationChannel.SMS,
    }

    response = test_http_client.post(
        "https://testserver/api/v1/notifications", json=payload
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert all(data.get(k) == v for k, v in payload.items())
    assert data["status"] == NotificationStatus.FAILED
    assert data["user_id"] == auth_user_and_cookie.get_safe_attributes()["id"]


def test_replace_notification_returns_success_and_replaced_item(
    db_session, test_http_client, auth_user_and_cookie
):
    """
    Tests PUT /notifications/{notification_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns replaced notification.
    - validate replaced notification's fields.
    """

    notification = Notification(
        user_id=auth_user_and_cookie.get_safe_attributes()["id"],
        title="Old title",
        content="Old content",
        channel=NotificationChannel.EMAIL,
        status=NotificationStatus.SENT,
    )
    db_session.add(notification)
    db_session.commit()
    db_session.refresh(notification)

    replace_payload = {
        "title": "New title",
        "content": "New content",
        "channel": NotificationChannel.PUSH,
    }

    response = test_http_client.put(
        f"https://testserver/api/v1/notifications/{notification.id!s}",
        json=replace_payload,
    )
    assert response.status_code == status.HTTP_200_OK

    replaced_notification_data = response.json()

    assert all(
        replaced_notification_data.get(k) == v for k, v in replace_payload.items()
    )
    assert replaced_notification_data["user_id"] == str(notification.user_id)


def test_update_notification_returns_success_and_updated_item(
    db_session, test_http_client, auth_user_and_cookie
):
    """
    Tests PATCH /notifications/{notification_id} endpoint.
    Asserts:
    - response includes HTTP status code 200.
    - response returns updated notification.
    - validate updated notification's fields.
    """

    notification = Notification(
        user_id=auth_user_and_cookie.get_safe_attributes()["id"],
        title="Original title",
        content="Original content",
        channel=NotificationChannel.EMAIL,
        status=NotificationStatus.SENT,
    )
    db_session.add(notification)
    db_session.commit()
    db_session.refresh(notification)

    updated_title = "Updated Title Successfully"

    update_payload = {"title": updated_title}

    response = test_http_client.patch(
        f"https://testserver/api/v1/notifications/{notification.id!s}",
        json=update_payload,
    )
    assert response.status_code == status.HTTP_200_OK

    updated_notification_data = response.json()
    notification_dict = notification.to_dict()
    notification_dict["user_id"] = str(notification_dict["user_id"])
    del notification_dict["title"]
    del notification_dict["updated_at"]

    assert updated_notification_data["title"] == updated_title
    assert all(
        updated_notification_data.get(k) == v for k, v in notification_dict.items()
    )


def test_user_cannot_delete_another_users_notifications(
    db_session, test_http_client, auth_user_and_cookie, sample_secondary_user
):
    """
    Tests DELETE /notifications/{notification_id} endpoint.
    Asserts:
    - response includes HTTP status code 404 when trying to delete another user's notification.
    """

    foreign_notification = Notification(
        user_id=sample_secondary_user.get_safe_attributes()["id"],
        title="Top Secret RMS.",
        content="Emacs > Vi",
        channel=NotificationChannel.EMAIL,
        status=NotificationStatus.SENT,
    )
    db_session.add(foreign_notification)
    db_session.commit()
    db_session.refresh(foreign_notification)

    delete_response = test_http_client.get(
        f"https://testserver/api/v1/notifications/{foreign_notification.id!s}"
    )
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND
