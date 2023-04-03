from rest_framework.response import Response
from rest_framework.test import APIClient
from storages.backends.s3boto3 import S3Boto3Storage


def read_img_content(file_path: str) -> bytes:
    """
    Helper function for tests.
    Read and return image content.
    :param file_path: path to image
    :return: image content
    """
    with open(file_path, "rb") as f:
        file_content = f.read()
    return file_content


def make_request_to_upload_image(
    client: APIClient, img_path: str, url: str, request_method: str
) -> Response:
    """
    Read image file and upload its content to minio
    using given request method.
    """
    with open(img_path, "rb") as f:
        method = getattr(client, request_method)
        response = method(url, data={"image": f})
    return response


def images_exist(
    image_names: list, user_id: int, storage: S3Boto3Storage
) -> list:
    """
    Check if images from given list are present
    in minio.
    :return: list of booleans for each image.
    If True, image exists, otherwise False.
    """
    are_existing = []
    for img_name in image_names:
        image_path = f"{user_id}/{img_name}"
        are_existing.append(storage.exists(image_path))
    return are_existing
