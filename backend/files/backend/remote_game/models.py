# remote_game/models.py

# from django.db import models
# from django.contrib.auth import get_user_model
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models

class RemoteGame(models.Model) :
	player1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='player1')
	player2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='player2')
	created_at = models.DateTimeField(auto_now_add=True)
	started_at = models.DateTimeField(null=True)
	numberofHitsP1 = models.IntegerField(default=0)
	numberofHitsP2 = models.IntegerField(default=0)
	gameDuration = models.DurationField(default=timedelta(minutes=0, seconds=0))
	winner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
	finished = models.BooleanField(default=False)
