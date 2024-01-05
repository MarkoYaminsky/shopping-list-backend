from app.common.models import BaseModel
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_superuser(self, username: str, password: str) -> "User":
        from app.users.services import create_user

        return create_user(username=username, password=password)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    phone_number = PhoneNumberField(region="UA", unique=True, null=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("password",)
    objects = UserManager()
