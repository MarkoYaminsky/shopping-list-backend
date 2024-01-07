from app.users.views import UserLoginAPI, UserRegistrationAPI, UserRegistrationCheckAPI
from django.urls import path

app_name = "users"

urlpatterns = [
    path("register/", UserRegistrationAPI.as_view(), name="user-registration"),
    path("register/check/", UserRegistrationCheckAPI.as_view(), name="user-registration-check"),
    path("login/", UserLoginAPI.as_view(), name="user-login"),
]
