from remote_game.models import RemoteGame
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
import json
# Create your models here.

class Tournament(models.Model):
  tournament_name = models.CharField(max_length=255)
  start_date = models.DateTimeField()
  finished_date = models.DateTimeField(default=None, null=True)
  finished = models.BooleanField(default=False)
  games = models.ManyToManyField(RemoteGame)
  
  def __str__(self):
    return self.tournament_name
  
  def to_dict(self, with_games=False):
    return {
        'id': self.id,
        'tournament_name': self.tournament_name,
        'start_date': self.start_date.isoformat(),
        'finished_date': self.finished_date.isoformat() if self.finished_date else None,
        'finished': self.finished,
        **({'games': [game.to_dict() for game in self.games.all()]} if with_games else {})
    }

  def to_json(self, with_games=False):
    return json.dumps(self.to_dict(with_games), cls=DjangoJSONEncoder)
  
  def queryset_to_json(queryset, with_games=False):
    tournaments_data = [tournament.to_dict(with_games) for tournament in queryset]
    return json.dumps(tournaments_data, cls=DjangoJSONEncoder)