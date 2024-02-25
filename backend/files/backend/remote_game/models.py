from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models

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

	def __str__(self):
		return str(self.pk)
	
	def return_all_data(self):
		return{
			'id': self.pk,
            'player1': self.player1.alias,
            'player2': self.player2.alias,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'finished_at': self.finished_at,
            'pointsP1': self.pointsP1,
            'pointsP2': self.pointsP2,
            'winner': self.winner.alias,
            'loser': self.loser.alias,
            'finished': self.finished,
		}