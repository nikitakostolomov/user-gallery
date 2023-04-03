from rest_framework import generics, permissions

from .serializers import RegisterUserSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]  # Or anon users can't register


register_user_api_view = RegisterUserAPIView.as_view()
