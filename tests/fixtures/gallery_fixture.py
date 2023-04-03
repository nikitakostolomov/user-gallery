import pytest
from storages.backends.s3boto3 import S3Boto3Storage

from .global_vars import IMAGE_DIR, IMG_1_NAME, IMG_1_PATH


@pytest.fixture(scope="package")
def storage():
    storage = S3Boto3Storage()
    yield storage


@pytest.fixture(scope="package")
def post_image_to_minio_without_user(storage):
    storage = S3Boto3Storage()
    with open(IMG_1_PATH, "rb") as f:
        storage.save(IMAGE_DIR, f)
    yield storage
    storage.bucket.objects.all().delete()


@pytest.fixture
def post_image_to_minio_with_user(request, storage, create_user):
    user = create_user
    try:
        # check if params were passed
        params = request.param
    except AttributeError:
        # if params were not passed
        # default image will be uploaded
        params = None
    if params is None:
        image_dir = f"{user.id}/{IMG_1_NAME}"
        with open(IMG_1_PATH, "rb") as f:
            storage.save(image_dir, f)
    else:
        for img_name, img_path in params.items():
            image_dir = f"{user.id}/{img_name}"
            with open(img_path, "rb") as f:
                storage.save(image_dir, f)

    yield storage, user

    storage.bucket.objects.all().delete()
