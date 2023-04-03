import pytest
from users.models import User

from .global_vars import ADMIN_USERNAME, PASSWORD, USERNAME


@pytest.fixture(scope="function")
def create_user():
    return User.objects.create_user(username=USERNAME, password=PASSWORD)
    # User.objects.all().delete()


@pytest.fixture(scope="function")
def create_superuser():
    return User.objects.create_superuser(
        username=ADMIN_USERNAME, password=PASSWORD
    )
    # User.objects.all().delete()
