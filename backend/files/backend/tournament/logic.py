from django.http import JsonResponse
from remote_game.models import RemoteGame
from django.contrib.auth import get_user_model
from remote_game.gameHandler import GameHandler
from remote_game.consumers import RemoteGameConsumer
from django.contrib.auth.models import AbstractUser
from remote_game.player import Player
from chat.consumers import ChatConsumer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from django.utils import timezone
from datetime import datetime
from .models import Tournament
import asyncio
import json

@sync_to_async
def get_user_by_username(username):
    return get_user_model().objects.get(username=username)


async def invite_to_tournament(user1, user):
  consumer = ChatConsumer()
  # check if the other user already invited this user
  print("hello\n")
  if user in await sync_to_async(list)(user1.game_invites_received.all()):
      # check if both player object exist
        # (player object is created when the user connects and deleted when the user disconnects)
    player1 = Player.get_player_by_user(user1)
    player2 = Player.get_player_by_user(user)
    if player1 == None or player2 == None:
      await consumer.save_and_send_message(user, user1, 'Player seems to be offline. Try again later.', datetime.now(), 'info')
      return
    # check if already playing
    # (a playing player has a game_handler attribute which is not None)
    if player1.game_handler != None or player2.game_handler != None:
      await consumer.save_and_send_message(user, user1, 'Player is already playing. Try again later.', datetime.now(), 'info')
      return
    # remove players from the waiting rooms
      # (to avoid multiple games running for the same players)
    game_consumer = RemoteGameConsumer()
    if player1 in game_consumer.training_waiting_room:
      game_consumer.training_waiting_room.remove(player1)
    if player1 in game_consumer.ranked_waiting_room:
      game_consumer.ranked_waiting_room.remove(player1)
    if player2 in game_consumer.training_waiting_room:
      game_consumer.training_waiting_room.remove(player2)
    if player2 in game_consumer.ranked_waiting_room:
      game_consumer.ranked_waiting_room.remove(player2)
    # send info message to both users
    await consumer.save_and_send_message(user, user1, 'You accepted the game invite.', datetime.now(), 'info')
    await consumer.save_and_send_message(user1, user, 'Game invite got accepted.', datetime.now(), 'info')
    # remove invites from both users
    await sync_to_async(user1.game_invites.remove)(user)
    await sync_to_async(user.game_invites.remove)(user1)
    # create a new game handler
    game_handler = await GameHandler.create(player1, player2, ranked=True)
    # open the game modal for both players
    await game_handler.channel_layer.group_send(
      game_handler.game_group,
      {
        'type': 'open_game_modal',
      })
    # start the game in another thread
    asyncio.ensure_future(game_handler.start_game())
    return
  # check if already invited
  if user in await sync_to_async(list)(user1.game_invites.all()):
    await consumer.save_and_send_message(user, user1, 'You already invited this user.', datetime.now(), 'info')
  else:
    # invite the other user
    await sync_to_async(user1.game_invites.add)(user)
    await consumer.save_and_send_message(user, user1, 'You sent a game invite.', datetime.now(), 'info')
    await consumer.save_and_send_message(user1, user, 'You got a game invite.', datetime.now(), 'info')

async def startTournament(request):
  if await sync_to_async(lambda: request.user.is_authenticated)():
    if request.method == 'POST':
      data = json.loads(request.body)
      User = get_user_model()
      print(len(data))
      print(data)
      number = await sync_to_async(Tournament.objects.count)()
      curr_tour = await sync_to_async(Tournament.objects.create)(tournament_name="Tournament" + str(number), start_date=timezone.now())
      total_games = len(data) - 1
      for match in range(total_games):
        # initiate games of the first round
        if match < total_games / 2:
          user1 = await get_user_by_username(data[match * 2]['name'])
          user2 = await get_user_by_username(data[match * 2 + 1]['name'])
          await invite_to_tournament(user1, user2)
        else:
          await invite_to_tournament(user1, user2)
      # Your existing code for tournament logic goes here
      # TODO: implement tournament logic
      # TODO: finished
      return JsonResponse({'message': 'Data received'})
    else:
      return JsonResponse({'error': 'Invalid request'}, status=400)