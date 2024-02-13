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
    alias = models.CharField(max_length=150, blank=True, null=True, verbose_name='Alias')
    is_42_login = models.BooleanField(default=False)
    num_games_played = models.IntegerField(default=0)
    num_games_won = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     # Rename file
    #     if self.profile_pic and self.profile_pic.name != "profilepic/default.jpeg":
    #         filename = self.profile_pic.name
    #         ext = filename[filename.rfind('.'):]
    #         new_filename = f"{self.username}{ext}"
    #         # print(f"--------------->save()")
    #         # print(f"--------------->save()_oldfilename:{self.profile_pic}")
    #         # print(f"--------------->save()_newfilename:{new_filename}")
    #         self.profile_pic.name = new_filename
    #     super().save(*args, **kwargs)

    # mobile = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.username
