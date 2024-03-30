from typing import Any

from app.common.types import SerializersWithBody, SerializersWithoutBody
from app.common.views import GetAPIView, PatchAPIView, PostAPIView, auto_extend_schema
from app.users.models import Profile
from app.users.serializers import (
    UserFullProfileRetrieveOutputSerializer,
    UserLoginInputSerializer,
    UserLoginOutputSerializer,
    UserProfileUpdateInputSerializer,
    UserRegistrationCheckInputSerializer,
    UserRegistrationInputSerializer,
)
from app.users.services import get_user_token, register_user, update_user_profile
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class UserRegistrationCheckAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationCheckInputSerializer

    @extend_schema(request=serializer_class, responses={status.HTTP_204_NO_CONTENT: None})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


@auto_extend_schema
class UserRegistrationAPI(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = SerializersWithBody(
        input=UserRegistrationInputSerializer,
    )

    def perform_action(self, username: str, password: str, **kwargs) -> None:
        register_user(username=username, password=password, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


@auto_extend_schema
class UserLoginAPI(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = SerializersWithBody(
        input=UserLoginInputSerializer,
        output=UserLoginOutputSerializer,
        response_status=status.HTTP_200_OK,
    )

    def perform_action(self, username: str, password: str) -> dict:
        return get_user_token(username=username, password=password)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


@auto_extend_schema
class UserFullProfileRetrieveAPI(GetAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_classes = SerializersWithoutBody(
        output=UserFullProfileRetrieveOutputSerializer,
        response_status=status.HTTP_200_OK,
    )

    def get_object(self, *args, **kwargs) -> User:
        return self.request.user

    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)


@auto_extend_schema
class UserProfileUpdateAPI(PatchAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_classes = SerializersWithBody(input=UserProfileUpdateInputSerializer)
    partial = True

    def get_object(self, *args, **kwargs) -> Any:
        return self.request.user

    def perform_action(self, update_object: Any, **kwargs) -> Any:
        update_user_profile(get_object_or_404(Profile, user=update_object), **kwargs)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)
