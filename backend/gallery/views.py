from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from storages.backends.s3boto3 import S3Boto3Storage

from .helpers import form_image_dir, raise_404_if_image_not_exist
from .mixins import UserQuerySetMixin
from .serializers import ImageQueryParamsSerializer, ImageSerializer


class GalleryAddGetDeleteImageAPIView(
    UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView
):
    parser_classes = [MultiPartParser]
    lookup_field = "pk"
    serializer_class = ImageQueryParamsSerializer

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ImageSerializer
        return self.serializer_class

    @swagger_auto_schema(query_serializer=ImageQueryParamsSerializer)
    def get(self, request, *args, **kwargs):
        file_dir, image_name = form_image_dir(
            request.query_params, request.user.pk
        )
        storage = S3Boto3Storage()
        raise_404_if_image_not_exist(storage, file_dir)
        return Response({image_name: storage.url(file_dir)})

    @swagger_auto_schema(query_serializer=ImageQueryParamsSerializer)
    def delete(self, request, *args, **kwargs):
        file_dir, _ = form_image_dir(request.query_params, request.user.pk)
        storage = S3Boto3Storage()
        raise_404_if_image_not_exist(storage, file_dir)
        storage.delete(file_dir)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        uploaded_image = ImageSerializer(data=request.data)
        if uploaded_image.is_valid(raise_exception=True):
            uploaded_image = uploaded_image.validated_data["image"]
            file_dir = f"{request.user.pk}/{uploaded_image.name}"
            storage = S3Boto3Storage()
            storage.save(file_dir, uploaded_image.file)
            return Response({uploaded_image.name: storage.url(file_dir)})


gallery_add_get_delete_image_view = GalleryAddGetDeleteImageAPIView.as_view()


class GalleryGetListImagesAPIView(UserQuerySetMixin, generics.ListAPIView):
    lookup_field = "pk"

    def list(self, request, *args, **kwargs):
        user_id = self.request.user.pk
        storage = S3Boto3Storage()
        _, images_list = storage.listdir(str(user_id))
        response = {}
        for image_name in images_list:
            image_dir = f"{user_id}/{image_name}"
            response[image_name] = storage.url(image_dir)
        return Response({"images": response})


gallery_get_list_images_view = GalleryGetListImagesAPIView.as_view()


class GalleryDeleteAllImagesAPIView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        storage = S3Boto3Storage()
        bucket = storage.bucket
        bucket.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


gallery_delete_all_images_view = GalleryDeleteAllImagesAPIView.as_view()
