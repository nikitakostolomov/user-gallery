from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path("register/", views.register_user_api_view, name="register-user"),
    path("auth/", obtain_auth_token),
]
