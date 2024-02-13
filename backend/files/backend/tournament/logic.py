from django.http import JsonResponse
from remote_game.models import RemoteGame
from django.contrib.auth import get_user_model
from remote_game.gameHandler import GameHandler
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Tournament
import json

def startTournament(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body)

      User = get_user_model()
      print("%d\n", len(data))

      number = Tournament.objects.count()
      curr_tour = Tournament.objects.create(tournament_name="Tournament" + str(number), start_date=timezone.now())

      placeholder1 = User.objects.get_or_create(username='test')[0]
      placeholder2 = User.objects.get_or_create(username='test')[0]

      total_games = len(data) - 1
      for match in range(total_games):
        #initiate games of the first round
        if match < total_games / 2:
          try:
              user1 = User.objects.get(username=data[match * 2]['name'])
          except User.DoesNotExist:
              return JsonResponse({'error': 'User does not exist'}, status=400)
          try:
              user2 = User.objects.get(username=data[match * 2 + 1]['name'])
          except User.DoesNotExist:
              return JsonResponse({'error': 'User does not exist'}, status=400)
          game_handler = async_to_sync(GameHandler.create)(user1, user2, ranked=True)
          game = game_handler.game
          curr_tour.games.add(game)
        else:
          game_handler = async_to_sync(GameHandler.create(placeholder1, placeholder2, ranked=True))
          game = game_handler.game
          curr_tour.games.add(game)


      # print(data);
      #TODO: implement tournament logic
      #TODO: finished
      return JsonResponse({'message': 'Data received'})
    else:
      return JsonResponse({'error': 'Invalid request'}, status=400)
