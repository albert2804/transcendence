from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import models
from django.contrib.auth import get_user_model
import json
import random
import asyncio
from .utils import PongGame

class RemoteGameConsumer(AsyncWebsocketConsumer):

    # map of connected players (user_id: channel_name)
    user_to_channel = {}
    channel_to_user = {}

    # group message handler
    async def message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
        }))
    
    async def add_to_waiting_group(self, channel_name):
        # following 2 lines are only for debugging
        username = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(RemoteGameConsumer.channel_to_user[channel_name])).username)()
        print(f"User {username} added to waiting group.")
        # add consumer to the group of waiting players
        await self.channel_layer.group_add("waiting", channel_name)
        # check if there is another player waiting
        if len(self.channel_layer.groups["waiting"]) >= 2:
            new_group_name = f"game_group_{random.randint(0, 1000000)}"
            waiting_channel_ids = list(self.channel_layer.groups["waiting"])
            if len(waiting_channel_ids) >= 2:
                await self.channel_layer.group_add(new_group_name, waiting_channel_ids[0])
                await self.channel_layer.group_discard("waiting", waiting_channel_ids[0])
                await self.channel_layer.group_add(new_group_name, waiting_channel_ids[1])
                await self.channel_layer.group_discard("waiting", waiting_channel_ids[1])
                # get usernames of the players
                first_player_username = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(RemoteGameConsumer.channel_to_user[waiting_channel_ids[0]])).username)()
                second_player_username = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(RemoteGameConsumer.channel_to_user[waiting_channel_ids[1]])).username)()
                # send message to the players
                await self.channel_layer.group_send(
                    new_group_name,
                    {
                        'type': 'message',
                        'message': f'The game is starting! Players: {first_player_username} vs. {second_player_username}',
                    }
                )
                # start the game
                print(f"Starting game with players {first_player_username} and {second_player_username}. Group name: {new_group_name}")
            else:
                # TODO:
                # remove the new created group
                del self.channel_layer.groups[new_group_name]
                await self.channel_layer.group_send(
                    f"user_{self.channel_to_user[channel_name]}",
                    {
                        'type': 'message',
                        'message': 'Something went wrong. Please try again.',
                    }
                )
        else:
            await self.channel_layer.group_send(
                f"user_{self.channel_to_user[channel_name]}",
                {
                    'type': 'message',
                    'message': 'Waiting for another player to join...',
                }
            )
    
    async def connect(self):
        await self.accept()
        if self.scope["user"].is_authenticated:
            # check if user is already connected
            if self.scope["user"].id in RemoteGameConsumer.user_to_channel:
                print(f"User {self.scope['user'].id} is already connected.")
                await self.send(text_data=json.dumps({
                    'type': 'message',
                    'message': 'You are already connected with another device.',
                }))
                await self.close()
                return
            print(f"User {self.scope['user']} connected.")
            #  add user to his own group / create group for the user
            await self.channel_layer.group_add(
                f"user_{self.scope['user'].id}",
                self.channel_name
            )
            # add user to the maps
            RemoteGameConsumer.user_to_channel[self.scope["user"].id] = self.channel_name
            RemoteGameConsumer.channel_to_user[self.channel_name] = self.scope["user"].id
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': 'Welcome!',
            }))
            await self.add_to_waiting_group(self.channel_name)
        
    async def disconnect(self, close_code):
        print(f"User {self.scope['user']} disconnected.")
        if self.scope["user"].is_authenticated:
            # remove user from the maps
            if self.scope["user"].id in RemoteGameConsumer.user_to_channel:
                del RemoteGameConsumer.user_to_channel[self.scope["user"].id]
            if self.channel_name in RemoteGameConsumer.channel_to_user:
                del RemoteGameConsumer.channel_to_user[self.channel_name]
            # remove user from the waiting group
            await self.channel_layer.group_discard("waiting", self.channel_name)
            # remove user from the game group
            groups_copy = list(self.channel_layer.groups.keys())
            for group_name in groups_copy:
                if group_name.startswith("game_group_"):
                    await self.channel_layer.group_discard(group_name, self.channel_name)
                    # kill the game if there is only one player left
                    if group_name in self.channel_layer.groups and len(self.channel_layer.groups[group_name]) == 1:
                        print(f"Killing game {group_name} because there is only one player left.")
                        # send message to the remaining player
                        await self.channel_layer.group_send(
                            group_name,
                            {
                                'type': 'message',
                                'message': 'The other player left the game. In 10 seconds you will be added to the waiting group.',
                            }
                        )
                        # wait 10 seconds
                        await asyncio.sleep(10)
                        # move the remaining player to the waiting group
                        if group_name in self.channel_layer.groups and len(self.channel_layer.groups[group_name]) == 1:
                            remaining_player_channel_id = list(self.channel_layer.groups[group_name])[0]
                            await self.add_to_waiting_group(remaining_player_channel_id)
                            del self.channel_layer.groups[group_name]












# class RemoteGameConsumer(AsyncWebsocketConsumer):
#     connected_players = 0

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.game = None

#     async def connect(self):
#         # await self.accept()
#         # print(f"upgrade to websocket accepted")
#         # # Start sending periodic game state updates
#         # asyncio.ensure_future(self.send_periodic_updates())
#         # print(f"periodic updates started")
#         # User = get_user_model()
#         # print(f"Welcome ", User)
#         # # player = User.objects.get(id=int())
#         # # print(f"Welcome ", player)
#         user = self.scope['user']
#         if user.is_authenticated:
#             await self.accept()
#             await self.send(text_data=json.dumps({
#                 'type': 'message',
#                 'message': 'Welcome!',
#             }))
#             group_name = "game"
#             await self.channel_layer.group_add(group_name, self.channel_name)
#             RemoteGameConsumer.connected_players += 1
#             if RemoteGameConsumer.connected_players % 2 == 1:
#                 self.player_role = 1
#             else:
#                 self.player_role = 2
#                 new_group_name = f"game_group_{RemoteGameConsumer.connected_players // 2}"
#                 await self.channel_layer.group_add(new_group_name, self.channel_name)

#                 # Überprüfe, ob beide Spieler in der neuen Gruppe sind
#                 if RemoteGameConsumer.connected_players % 2 == 0:
#                     # Benachrichtige beide Spieler, dass das Spiel startet
#                     await self.send(text_data=json.dumps({
#                         'type': 'message',
#                         'message': 'The game is starting!',
#                     }))

#                     # Starte das Spiel im Backend
#                     await self.start_game()
#         else:
#             await self.close()

#     # async def disconnect(self, close_code):
#     #     print(f"websocket connection closed")
#     #     # pass
#     #     if self.game is not None:
#     #         self.game.isGameExited = True
#     #     # self.game.isGameExited = True

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("game", self.channel_name)
#         if self.game is not None:
#             self.game.isGameExited = True
#         # Remove the player's role when disconnecting
#         if self.player_role == 2:
#             await self.channel_layer.group_discard(f"game_group_{GameConsumer.connected_players // 2}", self.channel_name)

#     async def receive(self, text_data):
#         try:
#             if self.game is not None:
#                 game_data = json.loads(text_data)
#                 print(f"game_data: {game_data}")
#                 type = game_data.get('type')
#                 key = game_data.get('key')
#                 print(f"Type: {type}, Key: {key}")
#                 if type == 'key_pressed':
#                     if key == 'ArrowUp':
#                         self.game.rightPaddle['dy'] = -2
#                     elif key == 'ArrowDown':
#                         self.game.rightPaddle['dy'] = 2
#                 elif type == 'key_released':
#                     if key in ['ArrowDown', 'ArrowUp']:
#                         self.game.rightPaddle['dy'] = 0
#                     # elif key == 'Escape':
#                     #     self.game.isGameExited=True
#                     #     self.close()
#             else:
#                 print("Game not initialized. Cannot receive game data.")
#         except json.JSONDecodeError:
#             print(f"Received invalid JSON file: {game_data}")
    
#     # async def start_game(self):
#     #     # Erstelle eine Instanz des Pong-Spiels
#     #     pong_game = PongGame()

#     #     # Starte das Spiel in einer Endlosschleife (game_loop)
#     #     while not pong_game.isGameExited:
#     #         pong_game.game_loop()

#     #         # Sende Spielstatus an die WebSocket-Verbindung der Spieler
#     #         await self.send_game_state()

#     #         # Warte für kurze Zeit, um die Geschwindigkeit des Spiels zu steuern
#     #         await asyncio.sleep(0.1)

#     #     # Spiel ist beendet, sende Endzustand an die WebSocket-Verbindung der Spieler
#     #     await self.send_game_state()
#     async def start_game(self):
#         self.game = PongGame()
#         if self.game is not None:
#             # Starte das Spiel in einer Endlosschleife (game_loop)
#             while not self.game.isGameExited:
#                 self.game.game_loop()

#                 # Sende Spielstatus an die WebSocket-Verbindung der Spieler
#                 await self.send_game_state()

#                 # Warte für kurze Zeit, um die Geschwindigkeit des Spiels zu steuern
#                 # await asyncio.sleep(0.1)
#                 asyncio.sleep(0.003)

#             # Spiel ist beendet, sende Endzustand an die WebSocket-Verbindung der Spieler
#             await self.send_game_state()
#         else:
#             print("Game not initialized. Cannot start the game.")
                
                
#     async def send_game_state(self):
#         if self.game is not None:
#             state = {
#                 'ball': {
#                     'x': self.game.ball['x'],
#                     'y': self.game.ball['y'],
#                     'radius': self.game.ball['radius'],
#                 },
#                 'leftPaddle': {
#                     'x': self.game.leftPaddle['x'],
#                     'y': self.game.leftPaddle['y'],
#                     'width': self.game.leftPaddle['width'],
#                     'height': self.game.leftPaddle['height'],
#                 },
#                 'rightPaddle': {
#                     'x': self.game.rightPaddle['x'],
#                     'y': self.game.rightPaddle['y'],
#                     'width': self.game.rightPaddle['width'],
#                     'height': self.game.rightPaddle['height'],
#                 },
#             }
#             high_score = {
#                 'numberOfHitsP1': self.game.numberOfHitsP1,
#                 'numberOfHitsP2': self.game.numberOfHitsP2,
#             }
#             await self.send(text_data=json.dumps({
#                 'type': 'game_update',
#                 'state': state,
#                 'high_score': high_score,
#             }))
#         else:
#             print("Game not initialized. Cannot send game state.")

#     # async def send_periodic_updates(self):
#     #     while not self.game.isGameExited:
#     #         # Update game state periodically
#     #         self.game.game_loop()
#     #         await self.send_game_state()

#     #         # Adjust the sleep duration based on your desired update frequency
#     #         await asyncio.sleep(0.003)  # Send updates every 0.002 second for a smooth UX