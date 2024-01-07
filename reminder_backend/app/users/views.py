from app.users.serializers import (
    UserRegistrationCheckInputSerializer,
    UserRegistrationInputSerializer,
)
from app.users.services import register_user
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class UserRegistrationCheckAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationCheckInputSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistrationAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationInputSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        register_user(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
