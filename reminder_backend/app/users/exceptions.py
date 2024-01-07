from rest_framework.exceptions import ValidationError


class UserWithPhoneNumberAlreadyExistsError(ValidationError):
    def __init__(self, phone_number: str) -> None:
        detail = f"User with phone_number {phone_number} already exists."
        super().__init__(detail=detail)


class NoAuthTokenError(ValidationError):
    def __init__(self, username: str) -> None:
        detail = f"User {username} has no authentication token."
        super().__init__(detail=detail)


class InvadlidCredentialsError(ValidationError):
    def __init__(self) -> None:
        detail = "Username or password is invalid."
        super().__init__(detail=detail)
