import pytest
from app.users.services import (
    create_user,
    get_all_users,
    get_user_by_phone_number,
    register_user,
)
from app.users.tests.factories import ProfileFactory, UserFactory
from django.contrib.auth import get_user_model

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
