from app.users.views import UserRegistrationAPI, UserRegistrationCheckAPI
from django.urls import path

app_name = "users"

urlpatterns = [
    path("register/", UserRegistrationAPI.as_view(), name="user-registration"),
    path("register/check", UserRegistrationCheckAPI.as_view(), name="user-registration-check"),
]
