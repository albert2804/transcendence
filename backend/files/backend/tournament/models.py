from django.db import models
from remote_game.models import RemoteGame
# Create your models here.

class Tournament(models.Model):
  tournament_name = models.CharField(max_length=255)
  start_date = models.DateTimeField()
  bracket = models.TextField()
  games = models.ManyToManyField(RemoteGame)
  
  def __str__(self):
    return self.tournament_name