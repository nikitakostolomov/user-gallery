import pytest
from django.http import Http404
from rest_framework.exceptions import ValidationError

from backend.gallery.helpers import (form_image_dir,
                                     raise_404_if_image_not_exist)
from tests.fixtures.global_vars import IMAGE_DIR, IMAGE_NAME, USER_ID


@pytest.mark.unit
@pytest.mark.parametrize(
    ["image_name", "expected_result"],
    [
        # string as image_name
        (IMAGE_NAME, (IMAGE_DIR, IMAGE_NAME)),
        # int as image_name
        (123, (f"{USER_ID}/123", "123")),
    ],
)
def test_form_image_dir(image_name, expected_result):
    """
    Test regular forming dir for image
    """
    result = form_image_dir({"image_name": image_name}, USER_ID)
    assert result == expected_result


@pytest.mark.unit
def test_form_image_dir_validation():
    """
    If query params do not contain image_name as key,
    ValidationError should be raised
    """
    with pytest.raises(ValidationError):
        form_image_dir({"abc": "my_image"}, USER_ID)


@pytest.mark.integration
def test_raise_404_if_image_not_exist(post_image_to_minio_without_user):
    """
    If file was not found, Http404 exception should be raised
    :param post_image_to_minio_without_user: post image to minio
    """
    storage = post_image_to_minio_without_user
    with pytest.raises(Http404):
        raise_404_if_image_not_exist(storage, "not/existing/directory")


@pytest.mark.integration
def test_not_raise_404_if_image_exist(post_image_to_minio_without_user):
    """
    If file was found, None should be returned
    :param post_image_to_minio_without_user: post image to minio
    """
    storage = post_image_to_minio_without_user
    result = raise_404_if_image_not_exist(storage, IMAGE_DIR)
    assert result is None
