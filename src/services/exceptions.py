from uuid import UUID


class UserNotFoundError(Exception):
    def __init__(self, user_id: UUID):
        super().__init__(self, f"User with id {user_id} does not exist.")


class InvalidPaginationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self, "Invalid pagination parameters. " + self.message)


class DatabaseConnectionError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self, "Database connection error. " + self.message)
