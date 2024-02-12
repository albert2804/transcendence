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
    chat_online = models.BooleanField(default=False)
    profile_pic = models.FileField(upload_to='profilepic', default ='profilepic/default.jpeg', blank=True, null=True)

    # mobile = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Rename the file before saving
        if self.profile_pic and self.profile_pic.name != "profilepic/default.jpeg":
            filename = self.profile_pic.name
            ext = filename[filename.rfind('.'):]
            new_filename = f"{self.username}{ext}"
            # print(f"--------------->save()")
            # print(f"--------------->save()_oldfilename:{self.profile_pic}")
            # print(f"--------------->save()_newfilename:{new_filename}")
            self.profile_pic.name = new_filename
            # print(f"--------------->after save():{self.profile_pic}")
        super().save(*args, **kwargs)
