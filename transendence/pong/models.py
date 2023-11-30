from django.db import models

# Create your models here.
class Games(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	description = models.TextField(null=True, blank = True)
	participants = 
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Players(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	description = models.TextField(null=True, blank = True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name
