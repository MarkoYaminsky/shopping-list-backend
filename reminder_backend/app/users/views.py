from app.common.types import RequestMethod, SerializersWithBody
from app.common.views import PostAPIView, auto_extend_schema
from app.users.serializers import (
    UserLoginInputSerializer,
    UserLoginOutputSerializer,
    UserRegistrationCheckInputSerializer,
    UserRegistrationInputSerializer,
)
from app.users.services import get_user_token, register_user
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegistrationCheckAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationCheckInputSerializer

    @extend_schema(request=serializer_class, responses={status.HTTP_204_NO_CONTENT: None})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


@auto_extend_schema(http_method=RequestMethod.POST)
class UserRegistrationAPI(PostAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = SerializersWithBody(
        input=UserRegistrationInputSerializer,
    )

    def perform_action(self, username: str, password: str, **kwargs) -> None:
        register_user(username=username, password=password, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


@auto_extend_schema(http_method=RequestMethod.POST)
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
