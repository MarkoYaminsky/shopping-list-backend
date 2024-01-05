import pytest
from app.users.services import create_user
from django.contrib.auth import get_user_model

User = get_user_model()


pytestmark = pytest.mark.django_db


class TestCreateUserService:
    username = "sashko"
    password = "rejected"

    def test_successful(self):
        user = create_user(username=self.username, password=self.password)

        assert User.objects.first() == user
