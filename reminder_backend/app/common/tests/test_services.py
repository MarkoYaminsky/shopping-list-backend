import pytest
from app.common.services import update_instance, update_instances
from app.users.tests.factories import ProfileFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestUpdateInstanceService:
    new_username = "Sasha"

    def test_no_fields(self):
        user = UserFactory()
        new_user_data = {"username": self.new_username}

        result = update_instance(data=new_user_data, instance=user)

        user.refresh_from_db()
        assert user.username == self.new_username
        assert result == (user, True)

    def test_with_fields(self):
        user = UserFactory()
        profile = ProfileFactory()
        new_user_data = {"username": self.new_username, "dog": "Bullet", "profile": profile}

        update_instance(data=new_user_data, fields=("username",), instance=user)

        assert user.username == self.new_username
        assert getattr(user, "profile", None) is None

    def test_with_non_existent_fields(self):
        non_existent_field_name = "data"
        user = UserFactory()

        update_instance(data={non_existent_field_name: "non_existent"}, instance=user)

        assert getattr(user, non_existent_field_name, None) is None

    def test_no_changes(self, user):
        instance, is_updated = update_instance(data={"username": user.username}, instance=user)

        assert is_updated is False
        assert instance == user


class TestUpdateMultipleInstancesService:
    update_data = {
        "username": "littlesasha",
        "display_name": "bigsasha",
        "status": "You've got to know life when married to a low-life",
    }

    def test_success(self, user):
        profile = ProfileFactory(user=user)

        update_instances(
            instances={user: ("username",), profile: ("display_name", "gender", "status", "phone_number")},
            data=self.update_data,
        )

        user.refresh_from_db()
        profile.refresh_from_db()
        assert user.username == self.update_data["username"]
        assert profile.display_name == self.update_data["display_name"]
        assert profile.status == self.update_data["status"]
