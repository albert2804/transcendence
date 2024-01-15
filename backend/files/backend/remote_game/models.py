# remote_game/models.py

from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta

class RemoteGame(models.Model) :
	player1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='player1')
	player2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='player2')
	created_at = models.DateTimeField(auto_now_add=True)
	numberofHitsP1 = models.IntegerField(default=0)
	numberofHitsP2 = models.IntegerField(default=0)
	gameDuration = models.DurationField(default=timedelta(minutes=0, seconds=0))
	winner = models.TextField()
