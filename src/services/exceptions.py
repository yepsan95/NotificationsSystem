from uuid import UUID


class UserNotFoundException(Exception):
    def __init__(self, user_id: UUID):
        super().__init__(self, f"User with id {user_id} does not exist.")
