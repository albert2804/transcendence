from django.http import JsonResponse
from remote_game.models import RemoteGame
from django.contrib.auth import get_user_model
from remote_game.gameHandler import GameHandler
from remote_game.consumers import RemoteGameConsumer
from django.contrib.auth.models import AbstractUser
from api.models import CustomUser
from remote_game.player import Player
from chat.consumers import ChatConsumer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from django.utils import timezone
from datetime import datetime
from .models import Tournament
import time
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import asyncio
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
    # user.set_password("Hallo9595");
    # user.save()
    user = CustomUser.objects.get_or_create(
      username="dummy2",
      password=make_password('Hallo9595'),
      alias="dummy2",
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

def readyPlayer(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body)
      user = get_user_by_username(data["username"])
      player = Player.get_player_by_user(user)
      if player.game_handler != None:
        return JsonResponse({'error': 'You have an active game'})
      game_consumer = RemoteGameConsumer()
      if player in game_consumer.training_waiting_room:
        game_consumer.training_waiting_room.remove(player)
      if player in game_consumer.ranked_waiting_room:
        game_consumer.ranked_waiting_room.remove(player)
      


      print(data)
      return JsonResponse({'message': 'Player is Ready'})
  else:
    return JsonResponse({'error': 'Invalid request'}, status=400)

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
            return JsonResponse({'error': f'Username {data["player"][match * 2]["name"]} does not exist'}, status=666)
          if user2 is None:
            return JsonResponse({'error': f'Username {data["player"][match * 2 + 1]["name"]} does not exit'}, status=666)
          game = RemoteGame.objects.create(
				    player1=user1,
				    player2=user2,
			    )
          curr_tour.games.add(game);
          game_list.append({'game_nbr': match, 'is_round': 1, 
                            'l_player': game.player1.username, 'r_player': game.player2.username, 
                            'l_score': game.pointsP1, 'r_score': game.pointsP2,})
          # await invite_to_tournament(user1, player1, user2, player2)
        else:
          game = RemoteGame.objects.create()
          game_list.append({'game_nbr': match, 
                            'is_round': math.floor(math.log2(total_games + 1)) - math.floor(math.log2(total_games - match)),
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
    
# async def invite_to_tournament(user1, player1, user2, player2):
  # consumer = ChatConsumer()

#   # check if the other user already invited this user
#   # if user in await sync_to_async(list)(user1.game_invites_received.all()):
#     # check if both player object exist
#       # (player object is created when the user connects and deleted when the user disconnects)
#   player1 = Player.get_player_by_user(user1)
#   player2 = Player.get_player_by_user(user2)
#   print("PLAYERS")
#   print(player1.user);
#   print(player2.user);
#   if player1 == None or player2 == None:
#     await consumer.save_and_send_message(user2, user1, 'Player seems to be offline. Try again later.', datetime.now(), 'info')
#     return
#   # check if already playing
#   # (a playing player has a game_handler attribute which is not None)
#   if player1.game_handler != None or player2.game_handler != None:
#     await consumer.save_and_send_message(user2, user1, 'Player is already playing. Try again later.', datetime.now(), 'info')
#     return
#   # remove players from the waiting rooms
#     # (to avoid multiple games running for the same players)
#   game_consumer = RemoteGameConsumer()
#   if player1 in game_consumer.training_waiting_room:
#     game_consumer.training_waiting_room.remove(player1)
#   if player1 in game_consumer.ranked_waiting_room:
#     game_consumer.ranked_waiting_room.remove(player1)
#   if player2 in game_consumer.training_waiting_room:
#     game_consumer.training_waiting_room.remove(player2)
#   if player2 in game_consumer.ranked_waiting_room:
#     game_consumer.ranked_waiting_room.remove(player2)
#   # send info message to both users
#   await consumer.save_and_send_message(user2, user1, 'You accepted the game invite.', datetime.now(), 'info')
#   await consumer.save_and_send_message(user1, user2, 'Game invite got accepted.', datetime.now(), 'info')
#   # remove invites from both users
#   await sync_to_async(user1.game_invites.remove)(user2)
#   await sync_to_async(user2.game_invites.remove)(user1)
#   # create a new game handler
#   game_handler = await GameHandler.create(player1, player2, ranked=False)
#   # open the game modal for both players
#   await game_handler.channel_layer.group_send(
#     game_handler.game_group,
#     {
#       'type': 'open_game_modal',
#     })
#   # start the game in another thread
#   asyncio.ensure_future(game_handler.start_game())
#   return
#   #check if already invited
#   #if user in await sync_to_async(list)(user1.game_invites.all()):
#   #  await consumer.save_and_send_message(user2, user1, 'You already invited this user.', datetime.now(), 'info')
#   #else:
#   # invite the other user
#   await sync_to_async(user1.game_invites.add)(user2)
#   await sync_to_async(user2.game_invites.add)(user1)
#   await consumer.save_and_send_message(user2, user1, 'You got a game invite.', datetime.now(), 'info')
#   await consumer.save_and_send_message(user1, user2, 'You got a game invite.', datetime.now(), 'info')