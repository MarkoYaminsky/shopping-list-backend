from app.users.models import Profile
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


def get_all_users(*args, **kwargs) -> QuerySet[User]:
    return User.objects.filter(*args, **kwargs)


def create_user(username: str, password: str, **kwargs) -> User:
    user = User.objects.create(username=username, **kwargs)
    user.set_password(password)
    user.save()
    return user


def register_user(username: str, password: str, **kwargs) -> User:
    user = create_user(username=username, password=password)
    profile = Profile.objects.create(user=user, **kwargs)
    return profile


def get_user_by_phone_number(phone_number: str) -> User:
    return get_all_users(profile__phone_number=phone_number).first()
