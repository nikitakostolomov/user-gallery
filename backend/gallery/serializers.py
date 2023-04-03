from rest_framework import serializers


class ImageQueryParamsSerializer(serializers.Serializer):
    image_name = serializers.CharField()


class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
