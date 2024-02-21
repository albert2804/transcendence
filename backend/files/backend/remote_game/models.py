from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json

class RemoteGame(models.Model) :
	player1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='player1', null=True, blank=True)
	player2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='player2', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	started_at = models.DateTimeField(null=True)
	finished_at = models.DateTimeField(null=True)
	pointsP1 = models.IntegerField(default=0)
	pointsP2 = models.IntegerField(default=0)
	winner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
	loser = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='games_lost')
	finished = models.BooleanField(default=False)
	# for the tournament
	player1_ready = models.BooleanField(default=False);
	player2_ready = models.BooleanField(default=False);
	# # if 0 then default game
	is_match_nbr = models.IntegerField(default=0)
	is_round = models.IntegerField(default=0)

	def to_dict(self):
		return {
      'id': self.id,
      'player1': self.player1.username if self.player1 else None,
      'player2': self.player2.username if self.player2 else None,
      'player1_ready': self.player1_ready,
      'player2_ready': self.player2_ready,
      'created_at': self.created_at.isoformat(),
      'started_at': self.started_at.isoformat() if self.started_at else None,
      'finished_at': self.finished_at.isoformat() if self.finished_at else None,
      'pointsP1': self.pointsP1,
      'pointsP2': self.pointsP2,
      'winner': self.winner.username if self.winner else None,
      'loser': self.loser.username if self.loser else None,
      'finished': self.finished,
			'is_round': self.is_round,
			'is_match': self.is_match_nbr,
    }
	
	def to_json(self):
		return json.dumps(self.to_dict(), cls=DjangoJSONEncoder)