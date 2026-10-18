import os
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

def user_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    user_role = 'admin' if (instance.is_staff or instance.is_superuser) else 'user'
    return os.path.join(f'users/{user_role}/', filename)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to=user_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    @property
    def is_individual(self) -> bool:
        return not self.memberships.exists()
