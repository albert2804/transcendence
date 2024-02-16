from django.db import models
from api.models import CustomUser

class Statistics(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	mmr = models.IntegerField(default=200)
	ranking = models.IntegerField(default=0)
    
	def __str__(self):
		return f"Statistics for {self.user.username}"