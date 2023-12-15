from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Already defined fields (from AbstractUser)
    # username
    # first_name
    # last_name
    # email
    # password
    # groups
    # user_permissions
    # is_staff
    # is_active
    # is_superuser
    # last_login
    # date_joined

    # Custom fields
    # profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    profile_pic = models.BinaryField(blank=True, null=True)
    # mobile = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.username
