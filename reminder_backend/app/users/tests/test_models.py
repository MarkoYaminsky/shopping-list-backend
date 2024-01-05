import pytest
from app.users.models import UserManager

pytestmark = pytest.mark.django_db


class TestUserManagerModel:
    password = "Po$mykay 4ndr1ya"
    username = "littlesasha"

    def test_create_superuser(self):
        manager = UserManager()

        user = manager.create_superuser(username=self.username, password=self.password)

        assert user.username == self.username
        assert user.check_password(self.password) is True
