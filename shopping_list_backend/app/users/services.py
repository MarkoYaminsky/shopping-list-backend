from app.common.services import update_instances
from app.users.exceptions import InvadlidCredentialsError, NoAuthTokenError
from app.users.models import Profile
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.authtoken.models import Token

User = get_user_model()


def get_all_users(*args, **kwargs) -> QuerySet[User]:
    return User.objects.filter(*args, **kwargs)


def create_user(username: str, password: str, **kwargs) -> User:
    user = User.objects.create(username=username, **kwargs)
    user.set_password(password)
    user.save()
    Token.objects.create(user=user)
    return user


def register_user(username: str, password: str, **kwargs) -> User:
    user = create_user(username=username, password=password)
    profile = Profile.objects.create(user=user, **kwargs)
    return profile


def get_user_by_phone_number(phone_number: str) -> User:
    return get_all_users(profile__phone_number=phone_number).first()


def get_user_token(username: str, password: str) -> dict:
    user = get_all_users(username=username).first()

    if not user.check_password(password):
        raise InvadlidCredentialsError

    user_token = user.token
    if user_token is None:
        raise NoAuthTokenError(username)

    return {"token": user_token.key}


def update_user_profile(profile: Profile, **kwargs) -> None:
    update_instances(
        instances={profile.user: ("username",), profile: ("display_name", "gender", "status", "phone_number")},
        data=kwargs,
    )
