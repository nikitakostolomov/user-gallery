from unittest.mock import patch

import pytest
from psycopg2 import Error
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from tests.fixtures.global_vars import PASSWORD, USERNAME

# test setup
client = APIClient()
pytestmark = pytest.mark.django_db


@pytest.mark.integration
@pytest.mark.parametrize(
    ["username", "http_method", "expected_status_code", "expected_response"],
    [
        # regular registration of new user
        ("Andrew", "post", 201, {"username": "Andrew"}),
        # user with given username already exists
        # should return unique error
        (
            USERNAME,
            "post",
            400,
            {"username": ["A user with that username already exists."]},
        ),
        # method other than post should return 405 status code
        (USERNAME, "get", 405, {"detail": 'Method "GET" not allowed.'}),
    ],
)
def test_register_user_view(
    create_user, username, http_method, expected_status_code, expected_response
):
    """
    Test regular save and save with not unique username
    :param create_user: fixture, that created user in db
    """
    url = reverse("register-user")
    data = {"username": username, "password": PASSWORD}
    call_method = getattr(client, http_method)
    response = call_method(path=url, data=data)

    assert response.status_code == expected_status_code
    assert response.data == expected_response


@pytest.mark.integration
@patch("users.serializers.User")
def test_register_user_db_error(create_user_mock):
    """
    Test exception handling, when something wrong with db
    :param create_user_mock: mock request to db. It will raise db exception
    """
    url = reverse("register-user")
    create_user_mock.objects.create_user.side_effect = Error
    response = client.post(
        path=url, data={"username": USERNAME, "password": PASSWORD}
    )
    assert response.data == {"error_message": "Something wrong with database"}
