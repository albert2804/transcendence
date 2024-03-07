from django.http import JsonResponse
from remote_game.models import RemoteGame
from api.models import CustomUser
from remote_game.player import Player
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from datetime import datetime
from .models import Tournament
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models import F
from chat.consumers import ChatConsumer
from django.core import serializers
import json
import math

def signUpTwoDummies(request):
  if request.method == 'POST':
    user = CustomUser.objects.get_or_create(
     username="dummy1",
     password=make_password('Hallo9595'),
     alias="dummy1",
     defaults={'email': "random@ass.de",
     'is_42_login': False,
     'chat_online': True, })
    user = CustomUser.objects.get_or_create(
      username="dummy2",
      password=make_password('Hallo9595'),
      alias="dummy2",
      defaults={'email': "random@ass.de",
      'is_42_login': False,
      'chat_online': True, })
    user = CustomUser.objects.get_or_create(
      username="phipno",
      password=make_password('Hallo9595'),
      alias="phipno",
      defaults={'email': "random@ass.de",
      'is_42_login': False,
      'chat_online': True, })
    return JsonResponse({'message': 'Data received'})
  else:
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_user_by_username(username):
    try:
        user = CustomUser.objects.get(username=username)
        return user
    except ObjectDoesNotExist:
      return None

def getPlayableGames(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      tournament_list = Tournament.objects.filter(Q(games__player1=request.user) | Q(games__player2=request.user))
      games_list = []

      for tournament in tournament_list:
        games = tournament.games.exclude(Q(player1=None) | Q(player2=None) | Q(finished=True)).filter(Q(player1=request.user) | Q(player2=request.user)).annotate(tournament_name=F('tournament__tournament_name'))
        for game in games:
          game.tournament_name = tournament.tournament_name
        games_list.extend(games)

      json_data = RemoteGame.queryset_to_json(games_list)
      # json_data = serializers.serialize('json', games_list, fields=('tournament_name',))
      return JsonResponse({'data': json_data})
  else:
    return JsonResponse({'error': 'Invalid request'}, status=400)

def getTourmaentsGames(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body);
      tournament = Tournament.objects.get(tournament_name=data["tournamentName"])
      json_data = Tournament.to_json(tournament, with_games=True)

      return JsonResponse({'data': json_data})
  else:
    return JsonResponse({'error': 'Invalid request'}, status=400)

def getTournaments(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body);
      ongoingOrEnded = data['ongoingOrEnded'];
      user = CustomUser.objects.get(username=data["name"])
      tournament_list = Tournament.objects.filter((Q(games__player1=user) | Q(games__player2=user)) & (Q(finished=ongoingOrEnded))).distinct()
      json_data = Tournament.queryset_to_json(tournament_list)

      return JsonResponse({'data': json_data})
  else:
    return JsonResponse({'error': 'Invalid request'}, status=400)

async def initiateGame(user1, user2, game, tour):
  channel_layer = get_channel_layer()
  await channel_layer.group_send('gameconsumer_' + str(user1.id), {
      'type': 'start_tournament_game',
      'user_id_1': user1.id,
      'user_id_2': user2.id,
      'db_game_id': game.id,
      'tour_id': tour.id,
    })

def inviteOtherPlayer(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body)
      user1 = get_user_by_username(data["username"])
      player1_handler = Player.get_player_by_user(user1)
      if player1_handler.game_handler is not None:
        return JsonResponse({'error': 'You have an active game'}, status=404)
      tour = Tournament.objects.get(tournament_name=data["tour_name"])
      if tour is None:
        return JsonResponse({'error': 'Sorry Tournament not Found'}, status=404)

      games = tour.games.all()
      game = games.get(is_match_nbr=data["game_nbr"])
      if game is None:
        return JsonResponse({'error': 'Sorry Game from Tournament not Found'}, status=404)
      if data["username"] == game.player1.username:
        user2 = get_user_by_username(game.player2)
      else:
        user2 = get_user_by_username(game.player1)
      if user2 is None:
        return JsonResponse({'error': 'User is missing in database'}, status=404)
      
      async_to_sync(initiateGame)(user1, user2, game, tour)
        
      
      return JsonResponse({'message': 'Player is Ready'})
  return JsonResponse({'error': 'Invalid request'}, status=400)

def initTournament(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body)
      consumer = ChatConsumer()

      tournament_count = Tournament.objects.filter(tournament_name__startswith=data["name"]).count()
      if tournament_count == 0:
        curr_tour = Tournament.objects.create(tournament_name=data["name"], start_date=timezone.now(), creator=request.user)
      else:
        curr_tour = Tournament.objects.create(tournament_name=data["name"] + str(tournament_count), start_date=timezone.now(), creator=request.user)

      total_games = len(data["player"]) - 1
      game_list = []
      for match in range(total_games):
        # initiate games of the first round
        if match <= total_games / 2:
          user1 = get_user_by_username(data["player"][match * 2]['name']);
          user2 = get_user_by_username(data["player"][match * 2 + 1]['name']);
          if user1 is None:
            return JsonResponse({'error': f'Username {data["player"][match * 2]["name"]} does not exist'}, status=400)
          if user2 is None:
            return JsonResponse({'error': f'Username {data["player"][match * 2 + 1]["name"]} does not exit'}, status=400)
          
          game = RemoteGame.objects.create(
                    player1=user1,
                    player2=user2,
            is_round= 1,
            is_match_nbr= match + 1,
                )
          curr_tour.games.add(game);
          game_list.append({'game_nbr': match, 'is_round': 1, 
                            'l_player': game.player1.username, 'r_player': game.player2.username, 
                            'l_score': game.pointsP1, 'r_score': game.pointsP2,})
          if curr_tour.creator != user1:
            async_to_sync(consumer.save_and_send_message)(curr_tour.creator, user1, curr_tour.creator.username + 'Created the tournament ' + curr_tour.tournament_name + ' and challengeses you.', datetime.now(), 'info')
          if curr_tour.creator != user2:
            async_to_sync(consumer.save_and_send_message)(curr_tour.creator, user2, curr_tour.creator.username + ' created the tournament ' + curr_tour.tournament_name + ' and challengeses you.', datetime.now(), 'info')

        else:
          game = RemoteGame.objects.create(
            is_round = math.floor(math.log2(total_games + 1)) - math.floor(math.log2(total_games - match)),
            is_match_nbr = match + 1,
          )
          game_list.append({'game_nbr': match, 'is_round': math.floor(math.log2(total_games + 1)) - math.floor(math.log2(total_games - match)),
                            'l_player': "", 'r_player': "",
                            'l_score': game.pointsP1, 'r_score': game.pointsP2,}) 
          curr_tour.games.add(game);
      data_curr_tour = {
        'tour_name': curr_tour.tournament_name,
        'games': game_list,
      }
      return JsonResponse({'data': data_curr_tour})
  else:
    return JsonResponse({'error': 'Invalid request'}, status=400)
