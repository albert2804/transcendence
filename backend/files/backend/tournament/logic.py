from django.http import JsonResponse
from remote_game.models import RemoteGame
from django.contrib.auth import get_user_model
from remote_game.gameHandler import GameHandler
from remote_game.consumers import RemoteGameConsumer
from django.contrib.auth.models import AbstractUser
from api.models import CustomUser
from channels.db import database_sync_to_async
from remote_game.player import Player
from chat.consumers import ChatConsumer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from django.utils import timezone
from datetime import datetime
from .models import Tournament
import time
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
import asyncio
import json
import math

import logging

logger = logging.getLogger(__name__)

def signUpTwoDummies(request):
  if request.method == 'POST':
    user = CustomUser.objects.get_or_create(
     username="dummy1",
     password=make_password('Hallo9595'),
     alias="dummy1",
     defaults={'email': "random@ass.de",
     'is_42_login': False,
     'chat_online': True, })
    # user.set_password("Hallo9595");
    # user.save()
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

def getTournaments(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body);
      user = CustomUser.objects.get(username=data["name"])
      tournament_list = Tournament.objects.filter(Q(games__player1=user) | Q(games__player2=user)).distinct()
      json_data = Tournament.queryset_to_json(tournament_list)

      return JsonResponse({'data': json_data})
  else:
    return JsonResponse({'error': 'Invalid request'}, status=400)

async def initiateGame(user1, user2, game):
  channel_layer = get_channel_layer()
  await channel_layer.group_send('gameconsumer_' + str(user1.id), {
      'type': 'start_tournament_game',
      'user_id_1': user1.id,
      'user_id_2': user2.id,
      'db_game_id': game.id,
    })

def readyPlayer(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body)
      print(data)
      user1 = get_user_by_username(data["username"])
      print(user1.username)
      player1_handler = Player.get_player_by_user(user1)
      if player1_handler.game_handler is not None:
        return JsonResponse({'error': 'You have an active game'}, status=404)
      
      game_consumer = RemoteGameConsumer()
      if player1_handler in game_consumer.training_waiting_room:
        game_consumer.training_waiting_room.remove(player1_handler)
      if player1_handler in game_consumer.ranked_waiting_room:
        game_consumer.ranked_waiting_room.remove(player1_handler)

      tour = get_object_or_404(Tournament, tournament_name=data["tour_name"])
      if tour is None:
        return JsonResponse({'error': 'Sorry Tournament not Found'}, status=404)

      games = tour.games.all()
      game = games.get(is_match_nbr=data["game_nbr"])
      print(game.id)
      if data["username"] == game.player1.username:
        game.player1_ready = True
      else:
        game.player2_ready = True
      print(game.player1_ready)
      print(game.player2_ready)
      game.save()
      if game.player1_ready and game.player2_ready:
        if data["username"] == game.player1.username:
          user2 = get_user_by_username(game.player2)
        else:
          user2 = get_user_by_username(game.player1)
        player2_handler = Player.get_player_by_user(user2)
        #return shit if not existing
        async_to_sync(initiateGame)(user1, user2, game)
        
      return JsonResponse({'message': 'Player is Ready'})
  return JsonResponse({'error': 'Invalid request'}, status=400)

# async def readyPlayer(request):
#   if request.method == 'POST':
#     data = json.loads(request.body)
#     print(data)
#     user1 = await sync_to_async(get_user_by_username)(data["username"])
#     print(user1.username)
#     player1_handler = await sync_to_async(Player.get_player_by_user)(user1)
#     if player1_handler.game_handler is not None:
#       return JsonResponse({'error': 'You have an active game'}, status=404)
    
#     game_consumer = RemoteGameConsumer()
#     if player1_handler in game_consumer.training_waiting_room:
#       game_consumer.training_waiting_room.remove(player1_handler)
#     if player1_handler in game_consumer.ranked_waiting_room:
#       game_consumer.ranked_waiting_room.remove(player1_handler)
#     tour = await sync_to_async(get_object_or_404)(Tournament, tournament_name=data["tour_name"])
#     if tour is None:
#       return JsonResponse({'error': 'Sorry Tournament not Found'}, status=404)
#     games = tour.games.all()
#     game = await sync_to_async(games.get)(is_match_nbr=data["game_nbr"])
#     print("FOURRIOUS")
#     player1 = await sync_to_async(getattr)(game, 'player1')
#     print(player1)
#     if data["username"] == player1.username:
#       game.player1_ready = True
#     else:
#       game.player2_ready = True
#     await sync_to_async(game.save)()
#     if game.player1_ready and game.player2_ready:
#       if data["username"] == player1.username:
#         player2 = await sync_to_async(getattr)(game, 'player2')
#         user2 = await sync_to_async(get_user_by_username)(player2.username)
#       else:
#         user2 = await sync_to_async(get_user_by_username)(player1.username)
#       player2_handler = await sync_to_async(Player.get_player_by_user)(user2)




#     return JsonResponse({'message': 'Player is Ready'})
#   return JsonResponse({'error': 'Invalid request'}, status=400)

def initTournament(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body)

      print(data)
      tournament_count = Tournament.objects.filter(tournament_name__startswith=data["name"]).count()
      print(tournament_count)
      if tournament_count == 0:
        curr_tour = Tournament.objects.create(tournament_name=data["name"], start_date=timezone.now())
      else:
        curr_tour = Tournament.objects.create(tournament_name=data["name"] + str(tournament_count), start_date=timezone.now())

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
          # await invite_to_tournament(user1, player1, user2, player2)
        else:
          game = RemoteGame.objects.create(
            is_round = math.floor(math.log2(total_games + 1)) - math.floor(math.log2(total_games - match)),
            is_match_nbr = match + 1,
          )
          game_list.append({'game_nbr': match, 'is_round': math.floor(math.log2(total_games + 1)) - math.floor(math.log2(total_games - match)),
                            'l_player': "", 'r_player': "",
                            'l_score': game.pointsP1, 'r_score': game.pointsP2,}) 
          curr_tour.games.add(game);
        # player1 = Player.get_player_by_user(user1);
        # player2 = Player.get_player_by_user(user2);
      # TODO: implement tournament logic
      # TODO: finished
      data_curr_tour = {
        'tour_name': curr_tour.tournament_name,
        'games': game_list,
      }
      return JsonResponse({'data': data_curr_tour})
  else:
    return JsonResponse({'error': 'Invalid request'}, status=400)
