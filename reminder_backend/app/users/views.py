from app.users.serializers import (
    UserRegistrationCheckInputSerializer,
    UserRegistrationInputSerializer,
)
from app.users.services import register_user
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


# TODO Add generic views with services
# TODO Add views for login
class UserRegistrationCheckAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationCheckInputSerializer

    @extend_schema(request=serializer_class, responses={status.HTTP_204_NO_CONTENT: None})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistrationAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationInputSerializer

    @extend_schema(request=serializer_class, responses={status.HTTP_204_NO_CONTENT: None})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        register_user(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
