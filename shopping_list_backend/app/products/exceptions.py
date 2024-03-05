from app.common.exceptions import BaseApiError


class CannotUpdatePositionNumberError(BaseApiError):
    def __init__(self) -> None:
        detail = f"Cannot update position number of product category directly."
        super().__init__(detail=detail, code="position-number-update")
