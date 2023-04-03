import pytest
import requests
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from tests.fixtures.global_vars import (IMG_1_NAME, IMG_1_PATH, IMG_2_NAME,
                                        IMG_2_PATH)
from tests.fixtures.helpers import (images_exist, make_request_to_upload_image,
                                    read_img_content)

# test setup
client = APIClient()
pytestmark = pytest.mark.django_db


@pytest.mark.integration
@pytest.mark.parametrize(
    ["image_name", "auth", "expected_status_code", "expected_file"],
    [
        # regular image retrieve, response with link
        # to saved image with 200 status code
        # should be returned
        (IMG_1_NAME, True, 200, read_img_content(IMG_1_PATH)),
        # if image does not exist, 404 status code
        # should be returned
        ("not_existing_image", True, 404, None),
        # if user is not authenticated, 401 status code
        # should be returned
        (IMG_1_NAME, False, 404, None),
    ],
)
def test_retrieve_image_view(
    post_image_to_minio_with_user,
    image_name,
    auth,
    expected_status_code,
    expected_file,
):
    """
    Test, that view will return file with status code 200,
    if user authenticated and image exists.
    Otherwise, other responses should be returned.
    :param post_image_to_minio_with_user: create user and
    post image to minio for created user
    :param image_name: name of the posted image
    :param auth: True if user should be authenticated for test
    otherwise False
    :param expected_status_code: status code, that
    should be returned by response
    :param expected_file: file, that should
    be retrieved
    """
    _, user = post_image_to_minio_with_user
    if auth:
        client.force_authenticate(user=user)
    else:
        client.force_authenticate()
    url = reverse("gallery-add-get-delete-image")

    response = client.get(url, data={"image_name": image_name})

    assert response.status_code == expected_status_code

    if expected_status_code == 200:
        file_by_link = requests.get(response.data[image_name]).content
        assert file_by_link == expected_file


@pytest.mark.integration
@pytest.mark.parametrize(
    ["image_name", "auth", "expected_status_code"],
    [
        # regular image deletion, empty response
        # with 204 status code should be returned
        (IMG_1_NAME, True, 204),
        # if image does not exist, 404 status code
        # should be returned
        ("not_existing_image", True, 404),
        # if user is not authenticated, 401 status code
        # should be returned
        (IMG_1_NAME, False, 401),
    ],
)
def test_delete_image_view(
    image_name, auth, expected_status_code, post_image_to_minio_with_user
):
    """
    Test, that view will delete image with status code 204,
    if user authenticated and image exists.
    Otherwise, other responses should be returned.
    :param post_image_to_minio_with_user: create user and
    post image to minio for created user
    :param image_name: name of the posted image
    :param auth: True if user should be authenticated for test
    otherwise False
    :param expected_status_code: status code, that
    should be returned by response
    """
    storage, user = post_image_to_minio_with_user
    if auth:
        client.force_authenticate(user=user)
    else:
        client.force_authenticate()

    if expected_status_code == 204:
        # check, that image exists
        assert all(images_exist([image_name], user.pk, storage))
    # client.delete(url, data=data}) passes data to body ???????
    url = reverse("gallery-add-get-delete-image") + f"?image_name={image_name}"

    response = client.delete(url)

    assert response.status_code == expected_status_code
    if expected_status_code == 204:
        # check, that image was deleted
        assert not any(images_exist([image_name], user.pk, storage))


@pytest.mark.integration
@pytest.mark.parametrize(
    ["auth", "expected_status_code", "expected_image"],
    [
        # regular save of image, should return 200
        # status code and upload image to minio
        (True, 200, read_img_content(IMG_1_PATH)),
        # if user is not authenticated, 401 status code
        # should be returned
        (False, 401, None),
    ],
)
def test_update_image_view(
    create_user, storage, auth, expected_status_code, expected_image
):
    """
    Test, that image will be uploaded to minio with
    right path and content, if user is authenticated.
    Otherwise, other responses should be returned.
    :param create_user: fixture, that created user in db
    :param storage: fixture, that gives access to minio
    :param auth: True if user should be authenticated for test
    otherwise False
    :param expected_status_code: status code, that
    should be returned by response
    :param expected_image: image, that
    should be uploaded to minio
    """
    user = create_user
    if auth:
        client.force_authenticate(user=user)
    else:
        client.force_authenticate()

    url = reverse("gallery-add-get-delete-image")
    response = make_request_to_upload_image(client, IMG_1_PATH, url, "put")

    assert response.status_code == expected_status_code

    if expected_status_code == 200:
        expected_object_path = f"{user.pk}/{IMG_1_NAME}"
        object_path = [key.key for key in storage.bucket.objects.all()][0]
        assert object_path == expected_object_path

        file_by_link = requests.get(response.data[IMG_1_NAME]).content
        assert file_by_link == expected_image


@pytest.mark.integration
@pytest.mark.parametrize(
    [
        "auth",
        "expected_status_code",
        "expected_images",
        "post_image_to_minio_with_user",
    ],
    [
        # regular retrieve of multiple images, should return 200
        # status code
        (
            True,
            200,
            [read_img_content(IMG_1_PATH), read_img_content(IMG_2_PATH)],
            {IMG_1_NAME: IMG_1_PATH, IMG_2_NAME: IMG_2_PATH},
        ),
        # if user is not authenticated,
        # empty response should be returned
        (False, 200, [], {IMG_1_NAME: IMG_1_PATH, IMG_2_NAME: IMG_2_PATH}),
    ],
    indirect=["post_image_to_minio_with_user"],
)
def test_get_list_images_view(
    post_image_to_minio_with_user, auth, expected_status_code, expected_images
):
    """
    Test, that view will return files with status code 200,
    if user authenticated and image exists.
    Otherwise, other responses should be returned.
    :param post_image_to_minio_with_user: create user and
    post image to minio for created user
    :param auth: True if user should be authenticated for test
    otherwise False
    :param expected_status_code: status code, that
    should be returned by response
    :param expected_images: images, that
    should be retrieved
    """
    storage, user = post_image_to_minio_with_user
    if auth:
        client.force_authenticate(user=user)
    else:
        client.force_authenticate()

    url = reverse("gallery-get-list-images")

    response = client.get(url)

    assert response.status_code == expected_status_code

    if expected_status_code == 200:
        files_by_link = []
        for link in response.data["images"].values():
            files_by_link.append(requests.get(link).content)

        assert files_by_link == expected_images


@pytest.mark.integration
@pytest.mark.parametrize(
    [
        "image_names",
        "auth",
        "auth_admin",
        "expected_status_code",
        "post_image_to_minio_with_user",
    ],
    [
        # regular deletion of multiple images
        # should return 204 status code
        # deletion will be performed by admin
        # admin is authed
        (
            [IMG_1_NAME, IMG_2_NAME],
            True,
            True,
            204,
            {IMG_1_NAME: IMG_1_PATH, IMG_2_NAME: IMG_2_PATH},
        ),
        # user without admin permission tries
        # to perform deletion
        # 403 status code should be returned
        # deletion will not be performed by user
        # user is authed
        (
            [IMG_1_NAME, IMG_2_NAME],
            True,
            False,
            403,
            {IMG_1_NAME: IMG_1_PATH, IMG_2_NAME: IMG_2_PATH},
        ),
        # not authed admin tries
        # to perform deletion
        # 401 status code should be returned
        # deletion will not be performed by admin
        # admin is not authed
        (
            [IMG_1_NAME, IMG_2_NAME],
            False,
            True,
            401,
            {IMG_1_NAME: IMG_1_PATH, IMG_2_NAME: IMG_2_PATH},
        ),
        # not authed user tries
        # to perform deletion
        # 401 status code should be returned
        # deletion will not be performed by user
        # user is not authed
        (
            [IMG_1_NAME, IMG_2_NAME],
            False,
            False,
            401,
            {IMG_1_NAME: IMG_1_PATH, IMG_2_NAME: IMG_2_PATH},
        ),
    ],
    indirect=["post_image_to_minio_with_user"],
)
def test_delete_images_as_admin_view(
    image_names,
    auth,
    auth_admin,
    expected_status_code,
    post_image_to_minio_with_user,
    create_superuser,
):
    """
    Test, that view will delete all images with status code 204,
    if admin authenticated.
    Otherwise, other responses should be returned.
    :param post_image_to_minio_with_user: create user and
    post image to minio for created user
    :param create_superuser: create admin user
    :param image_names: list of posted images
    :param auth: True if user should be authenticated for test
    otherwise False
    :param auth_admin: True if admin should be authenticated for test
    otherwise False
    :param expected_status_code: status code, that
    should be returned by response
    """
    storage, user = post_image_to_minio_with_user
    user_with_images_id = user.pk
    admin = create_superuser
    if auth_admin:
        user = admin
    if auth:
        client.force_authenticate(user=user)
    else:
        client.force_authenticate()
    if expected_status_code == 204:
        # check, that image exists
        assert all(images_exist(image_names, user_with_images_id, storage))

    url = reverse("gallery-delete-all-images")

    response = client.delete(url)

    assert response.status_code == expected_status_code
    if expected_status_code == 204:
        assert not any(images_exist(image_names, user_with_images_id, storage))
