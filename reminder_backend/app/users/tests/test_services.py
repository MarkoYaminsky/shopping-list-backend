import pytest
from app.users.exceptions import InvadlidCredentialsError, NoAuthTokenError
from app.users.services import (
    create_user,
    get_all_users,
    get_user_by_phone_number,
    get_user_token,
    register_user,
)
from app.users.tests.factories import ProfileFactory, UserFactory
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestCreateUserService:
    username = "sashko"
    password = "rejected"

    def test_successful(self):
        user = create_user(username=self.username, password=self.password)

        assert User.objects.first() == user


class TestRegisterUserService:
    username = "sashko"
    password = "55337d77380674524276Sanek9class"
    display_name = "littlesasha"

    def test_successful(self):
        profile = register_user(username=self.username, password=self.password, display_name=self.display_name)

        assert profile.user.username == self.username
        assert profile.user.check_password(self.password) is True
        assert profile.display_name == self.display_name
        assert profile.user.auth_token is not None


class TestGetAllUsersService:
    users_count = 2

    def test_without_kwargs(self):
        UserFactory.create_batch(size=self.users_count)

        users = get_all_users()

        assert users.count() == self.users_count

    def test_with_kwargs(self):
        username = "littlesasha"
        user = UserFactory(username=username)
        UserFactory()

        users = get_all_users(username=username)

        assert users.count() == 1
        assert users.first() == user


class TestGetUserByPhoneNumberService:
    phone_number = "+380981033863"

    def test_success(self):
        ProfileFactory(phone_number="+380634892933")
        profile = ProfileFactory(phone_number=self.phone_number)

        user = get_user_by_phone_number(phone_number=self.phone_number)

        assert user == profile.user


class TestGetUserTokenService:
    password = "hello"

    @pytest.fixture
    def user_with_password(self, db) -> User:
        user = UserFactory()
        user.set_password(self.password)
        user.save()
        return user

    def test_user_has_token(self, user_with_password):
        Token.objects.create(user=user_with_password)

        token = get_user_token(username=user_with_password.username, password=self.password)

        assert token == {"token": user_with_password.token.key}

    def test_user_has_no_token(self, user_with_password):
        with pytest.raises(NoAuthTokenError, match=f"User {user_with_password.username} has no authentication token."):
            get_user_token(username=user_with_password.username, password=self.password)

    def test_invalid_password(self, user_with_password):
        with pytest.raises(InvadlidCredentialsError):
            get_user_token(username=user_with_password.username, password="1")
