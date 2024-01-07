from app.users.exceptions import UserWithPhoneNumberAlreadyExistsError
from app.users.services import get_user_by_phone_number
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class UserRegistrationCheckInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class UserRegistrationInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    phone_number = PhoneNumberField(region="UA", required=False)
    display_name = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    def validate_phone_number(self, phone_number: str) -> None:
        if phone_number is not None and get_user_by_phone_number(phone_number) is not None:
            raise UserWithPhoneNumberAlreadyExistsError(phone_number)
