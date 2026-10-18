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
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to=user_image_path, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
