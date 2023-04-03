from rest_framework import serializers
from users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user

    class Meta:
        model = User
        fields = ("username", "password")
