from typing import Optional

from app.common.models import BaseModel
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_superuser(self, username: str, password: str) -> "User":
        from app.users.services import create_user

        return create_user(username=username, password=password, is_staff=True, is_superuser=True)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("password",)
    objects = UserManager()

    @property
    def token(self) -> Optional[Token]:
        return getattr(self, "auth_token", None)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=128, blank=True)
    phone_number = PhoneNumberField(region="UA", unique=True, blank=True, null=True, default=None)
