from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models

class RemoteGame(models.Model) :
	player1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='player1')
	player2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='player2')
	created_at = models.DateTimeField(auto_now_add=True)
	started_at = models.DateTimeField(null=True)
	finished_at = models.DateTimeField(null=True)
	pointsP1 = models.IntegerField(default=0)
	pointsP2 = models.IntegerField(default=0)
	winner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
	loser = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='games_lost')
	finished = models.BooleanField(default=False)
