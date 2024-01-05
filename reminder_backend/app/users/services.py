from django.contrib.auth import get_user_model

User = get_user_model()


def create_user(username: str, password: str, **kwargs) -> User:
    user = User.objects.create(username=username, **kwargs)
    user.set_password(password)
    return user
