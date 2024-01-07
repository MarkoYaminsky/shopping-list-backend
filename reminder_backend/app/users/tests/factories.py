from app.users.models import Profile
from django.contrib.auth import get_user_model
from factory import Sequence, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = Sequence(lambda x: f"{fake.user_name()}{x}")
    password = "sashko"


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = SubFactory(UserFactory)
