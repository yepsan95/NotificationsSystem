from uuid import UUID


class UserNotFoundError(Exception):
    def __init__(self, user_id: UUID):
        super().__init__(self, f"User with id {user_id} not found.")


class UserInvalidPasswordError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self, "Invalid password. " + self.message)


class UserEmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(
            self, f"Email '{self.email}' is already taken by another user."
        )


class InvalidPaginationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self, "Invalid pagination parameters. " + self.message)


class DatabaseConnectionError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self, "Database connection error. " + self.message)


class InvalidRefreshTokenError(Exception):
    def _init__(self, message: str):
        self.message = message
        super().__init__(self, "Refresh token not found. " + self.message)


class ExpiredRefreshTokenError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self, "Refresh token's expiration date has passed. " + self.message)


class CompromisedSessionError(Exception):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        super().__init__(self, f"Compromised session. All tokens must be revoked for user with id '{user_id}'.")
