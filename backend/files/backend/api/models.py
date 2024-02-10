from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
	# Custom fields
	chat_online = models.BooleanField(default=False)
	profile_pic = models.FileField(upload_to='profilepic', default='profilepic/default.jpeg', blank=True, null=True)
	alias = models.CharField(max_length=150, blank=True, null=True, verbose_name='Alias')

	# mobile = models.CharField(max_length=20, blank=True, null=True)
	def __str__(self):
		return self.username
