from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model with profile picture
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)  # Field for phone number