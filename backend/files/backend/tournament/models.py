from remote_game.models import RemoteGame
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import json
# Create your models here.

class Tournament(models.Model):
  tournament_name = models.CharField(max_length=255)
  start_date = models.DateTimeField()
  games = models.ManyToManyField(RemoteGame)
  
  def __str__(self):
    return self.tournament_name
  
  def to_dict(self):
    return {
      'id': self.id,
      'tournament_name': self.tournament_name,
      'start_date': self.start_date.isoformat(),
      'games': [game.to_dict() for game in self.games.all()]
    }

  def to_json(self):
    return json.dumps(self.to_dict(), cls=DjangoJSONEncoder)
  
  def queryset_to_json(queryset):
    tournaments_data = [tournament.to_dict() for tournament in queryset]
    return json.dumps(tournaments_data, cls=DjangoJSONEncoder)