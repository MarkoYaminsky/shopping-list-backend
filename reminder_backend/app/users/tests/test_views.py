import pytest
from app.users.tests.factories import ProfileFactory, UserFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db

User = get_user_model()


class TestUserRegistrationCheckAPI:
    ROUTE = "users:user-registration-check"
    username = "littlesasha"

    def test_check_failed(self, api_client):
        UserFactory(username=self.username)

        response = api_client.post(reverse(self.ROUTE), data={"username": self.username})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_check_passed(self, api_client):
        response = api_client.post(reverse(self.ROUTE), data={"username": self.username})

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestUserRegistrationAPI:
    ROUTE = "users:user-registration"
    username = "littlesasha"
    password = "Ella Fitzgerald!123"
    display_name = "sasha"

    def test_invalid_phone_number(self, api_client):
        phone_number = "+380634892933"
        ProfileFactory(phone_number=phone_number)

        response = api_client.post(
            reverse(self.ROUTE),
            data={
                "username": self.username,
                "password": self.password,
                "display_name": self.display_name,
                "phone_number": phone_number,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["phone_number"] == [f"User with phone_number {phone_number} already exists."]

    def test_user_registered(self, api_client):
        response = api_client.post(
            reverse(self.ROUTE),
            data={"username": self.username, "password": self.password, "display_name": self.display_name},
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.username == self.username
        assert user.check_password(self.password) is True
        assert user.profile.display_name == self.display_name


class TestUserLoginAPI:
    ROUTE = "users:user-login"
    password = "11111"

    def test_success(self, api_client):
        user = UserFactory()
        token = Token.objects.create(user=user).key
        user.set_password(self.password)
        user.save()

        response = api_client.post(reverse(self.ROUTE), data={"username": user.username, "password": self.password})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"token": token}
