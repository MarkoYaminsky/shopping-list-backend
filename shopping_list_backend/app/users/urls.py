from app.users.views import (
    UserFullProfileRetrieveAPI,
    UserLoginAPI,
    UserProfileUpdateAPI,
    UserRegistrationAPI,
    UserRegistrationCheckAPI,
)
from django.urls import path

app_name = "users"

urlpatterns = [
    path("register/", UserRegistrationAPI.as_view(), name="user-registration"),
    path("register/check/", UserRegistrationCheckAPI.as_view(), name="user-registration-check"),
    path("login/", UserLoginAPI.as_view(), name="user-login"),
    path("profiles/my/", UserFullProfileRetrieveAPI.as_view(), name="my-profile-retrieve"),
    path("profiles/my/update/", UserProfileUpdateAPI.as_view(), name="my-profile-update"),
]
