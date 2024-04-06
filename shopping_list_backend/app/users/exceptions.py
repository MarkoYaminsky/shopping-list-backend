from app.common.exceptions import BaseApiError


class UserWithPhoneNumberAlreadyExistsError(BaseApiError):
    def __init__(self, phone_number: str) -> None:
        detail = f"User with phone_number {phone_number} already exists."
        super().__init__(detail=detail, code="unique-phone-number")


class NoAuthTokenError(BaseApiError):
    def __init__(self, username: str) -> None:
        detail = f"User {username} has no authentication token."
        super().__init__(detail=detail, code="no-user-auth-token")


class InvadlidCredentialsError(BaseApiError):
    def __init__(self) -> None:
        detail = "Username or password is invalid."
        super().__init__(detail=detail, code="user-login-credentials")
