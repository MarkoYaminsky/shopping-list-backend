import pytest
from app.users.models import UserManager
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db


class TestUserManagerModel:
    password = "Po$mykay 4ndr1ya"
    username = "littlesasha"

    def test_create_superuser(self):
        manager = UserManager()

        user = manager.create_superuser(username=self.username, password=self.password)

        assert user.username == self.username
        assert user.check_password(self.password) is True
        assert user.is_staff is True
        assert user.is_superuser is True


class TestUserModel:
    password = "Po$mykay 4ndr1ya"
    username = "littlesasha"

    def test_token_absent(self, user):
        token = user.token

        assert token is None

    def test_token_present(self, user):
        expected_token = Token.objects.create(user=user)

        token = user.token

        assert token == expected_token
