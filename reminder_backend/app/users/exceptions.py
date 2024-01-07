from rest_framework.exceptions import ValidationError


class UserWithPhoneNumberAlreadyExistsError(ValidationError):
    def __init__(self, phone_number: str) -> None:
        detail = f"User with phone_number {phone_number} already exists."
        super().__init__(detail=detail)
