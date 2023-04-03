from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    gallery_link = models.ImageField(null=True)
