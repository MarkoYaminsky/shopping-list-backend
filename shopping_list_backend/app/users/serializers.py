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


class UserLoginInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserLoginOutputSerializer(serializers.Serializer):
    token = serializers.CharField()


class UserFullProfileRetrieveOutputSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source="profile.display_name")
    phone_number = serializers.CharField(source="profile.phone_number")
    gender = serializers.CharField(source="profile.gender")
    status = serializers.CharField(source="profile.status")

    class Meta:
        model = User
        fields = ("id", "username", "display_name", "phone_number", "gender", "status")


class UserProfileUpdateInputSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()
    status = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "display_name", "phone_number", "gender", "status")

    def validate_phone_number(self, phone_number: str) -> None:
        user_with_existent_phone = get_user_by_phone_number(phone_number)
        if (
            phone_number is not None
            and user_with_existent_phone is not None
            and user_with_existent_phone != self.instance
        ):
            raise UserWithPhoneNumberAlreadyExistsError(phone_number)


class UserShortOutputSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source="profile.display_name")

    class Meta:
        model = User
        fields = ("id", "username", "display_name")