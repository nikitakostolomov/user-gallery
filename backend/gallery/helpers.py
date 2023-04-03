from typing import Tuple

from django.http import Http404
from storages.backends.s3boto3 import S3Boto3Storage

from .serializers import ImageQueryParamsSerializer


def form_image_dir(query_params: dict, user_id: int) -> Tuple[str, str]:
    """
    1. Validate, that query params contain image name.
    2. Form minio image dir, where image can be placed or deleted.
    Image dir has following the pattern: user_id/image_name
    E.g. "1/my_image"
    3. Return parsed image dir and image name
    :param query_params: dict with image name
        E.g. {"image_name": "my_image"}
    :param user_id: id of user, that sent request
    :return: tuple of formed minio image dir and image name
        E.g. ("1/my_image", "my_image")
    """
    query_params = ImageQueryParamsSerializer(data=query_params)
    if query_params.is_valid(raise_exception=True):
        image_name = query_params.validated_data["image_name"]
        image_dir = f"{user_id}/{image_name}"
        return image_dir, image_name


def raise_404_if_image_not_exist(storage: S3Boto3Storage, file_dir: str):
    """
    By default, django storages do not raise exception,
    if object in minio does not exist.
    In logic of this app, it should be raised.
    """
    if not storage.exists(file_dir):
        raise Http404()
