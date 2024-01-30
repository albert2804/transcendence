from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import models
from django.contrib.auth import get_user_model
import json
import random
import asyncio
from .utils import PongGame
from channels.layers import get_channel_layer

# TODO: send user object or id instead of p1_channel and p2_channel to GameGroup.
#       this way the game can be continued if the user disconnects and reconnects
#       (the user object is still the same, but the channel name changes)
#       -> we can still send messages to the user with his private channel name (f"game_user_{user.id}")
#       -> also we don't need to use the "channel_to_user" from RemoteGameConsumer here in GameGroup !

# TODO: In Frontend: if websocket connection is closed -> show message "Connection lost. Please reload the page."
#       hmm maybe send a disconnection code to the frontend and show a message there (for example if the user is already connected with another device)
#       google about close_code for the disconnect function ;)

# TODO: maybe implement a static function in the Player class to remove a player from the list of all players
#       so we can stop the game automatically if the user disconnects
#       Other idea: do not delete the player from the list of all players directly, but "pause" the game and wait for the user to reconnect

# TODO: implement send() function in GameGroup to send to both players. maybe other name for this function?


class Player:
    all_players = []

    @classmethod
    def get_player_by_channel(cls, channel):
        for player in Player.all_players:
            if player.get_channel() == channel:
                return player
        return None

    @classmethod
    def get_channel_by_user(cls, user):
        for player in Player.all_players:
            if player.get_user() == user:
                return player.get_channel()
        return None

    def __init__(self, user, channel):
        self.user = user
        self.channel = channel
        self.channel_layer = get_channel_layer()
        self.game_group = None
        Player.all_players.append(self)
    
    def get_user(self):
        return self.user
    
    def get_channel(self):
        return self.channel
    
    def change_channel(self, channel): # THIS CAN BE HELPFUL IF THE USER RECONNECTS OR WANTS TO PLAY ON ANOTHER DEVICE
        # check if player is in a game group
        # if self.game_group != None:
            # change channel in game group
            # self.channel_layer.group_discard(self.game_group, self.channel)
            # self.channel_layer.group_add(self.game_group, channel)
        # change channel in player object
        self.channel = channel
    
    async def add_to_game_group(self, game_group):
        self.game_group = game_group
        await self.channel_layer.group_add(
            self.game_group,
            self.channel
        )
    
    # async def remove_from_game_group(self):  # Maybe later needed in change_channel() ??
    #     await self.channel_layer.group_discard(
    #         self.game_group,
    #         self.channel
    #     )
    #     self.game_group = None
    
    def get_game_group(self):
        return GameHandler.get_game_group_by_name(self.game_group)
    
    async def send(self, message):
        await self.channel_layer.send(self.channel, message)

    


class GameHandler:
    all_game_groups = {}

    # Use create() instead of __init__() to create a new instance of this class 
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.game_group = f"game_{random.randint(0, 1000000)}"
        self.game = PongGame()
        self.channel_layer = get_channel_layer()
        GameHandler.all_game_groups[self.game_group] = self

    @classmethod
    async def create(cls, player1, player2):
        instance = cls(player1, player2)
        await player1.add_to_game_group(instance.game_group)
        await player2.add_to_game_group(instance.game_group)
        return instance
    
    @classmethod
    def get_game_group_by_name(cls, game_group_name):
        return GameHandler.all_game_groups.get(game_group_name, None)

    async def start_game(self):
        print(f"Started {self.game_group} between {self.player1.get_user().username} and {self.player2.get_user().username}.")
        # send info, that game is starting
        await self.channel_layer.group_send(
            self.game_group,
            {
                'type': 'state',
                'state': "playing",
                'p1_name': self.player1.get_user().username,
                'p2_name': self.player2.get_user().username,
            }
        )
        # run game loop
        while not self.game.isGameExited:
            self.game.game_loop()
            await self.send_game_state()
            await asyncio.sleep(0.003)
        # send info, that game is finished
        if (self.game.winner == 0):
            await self.channel_layer.group_send(
                self.game_group,
                {
                    'type': 'state',
                    'state': "finished",
                    'p1_name': "",
                    'p2_name': "",
                }
            )
        elif (self.game.winner == 1):
            # player 1 won
            await self.player1.send({
                'type': 'winner',
            })
            await self.player2.send({
                'type': 'loser',
            })
        elif (self.game.winner == 2):
            await self.player1.send({
                'type': 'loser',
            })
            await self.player2.send({
                'type': 'winner',
            })
        print(f"{self.game_group} between {self.player1.get_user().username} and {self.player2.get_user().username} finished.")
        # wait 5 seconds
        await asyncio.sleep(5)
        # send info, that game is finished and players are back in the menu
        await self.channel_layer.group_send(
            self.game_group,
            {
                'type': 'state',
                'state': "menu",
                'p1_name': "",
                'p2_name': "",
            }
        )
        del GameHandler.all_game_groups[self.game_group]
        del self
    
    def stop_game(self):
        # print(f"Stopped game ({self.game_group}) between {self.player1.get_user().username} and {self.player2.get_user().username}.")
        self.game.isGameExited = True
    
    def update_paddle(self, player, key, type):
        if player == self.player1:
            if type == 'key_pressed':
                if key == 'ArrowUp':
                    self.game.leftPaddle['dy'] = -2
                elif key == 'ArrowDown':
                    self.game.leftPaddle['dy'] = 2
            elif type == 'key_released':
                if key in ['ArrowDown', 'ArrowUp']:
                    self.game.leftPaddle['dy'] = 0
        elif player == self.player2:
            if type == 'key_pressed':
                if key == 'ArrowUp':
                    self.game.rightPaddle['dy'] = -2
                elif key == 'ArrowDown':
                    self.game.rightPaddle['dy'] = 2
            elif type == 'key_released':
                if key in ['ArrowDown', 'ArrowUp']:
                    self.game.rightPaddle['dy'] = 0
        else:
            print(f"Unknown player: {player}")
    
    async def send_game_state(self):
        state = {
            'ball': {
                'x': self.game.ball['x'],
                'y': self.game.ball['y'],
                'radius': self.game.ball['radius'], #needed?? BETTER PADDLESIZE IN PERCENT !!!
            },
            'leftPaddle': {
                'y': self.game.leftPaddle['y'],
            },
            'rightPaddle': {
                'y': self.game.rightPaddle['y'],
            },
        }
        high_score = {
            'numberOfHitsP1': self.game.numberOfHitsP1,
            'numberOfHitsP2': self.game.numberOfHitsP2,
        }
        # send game state to game group
        await self.channel_layer.group_send(
            self.game_group,
            {
                'type': 'game_update',
                'state': state,
                'high_score': high_score,
            }
        )

class RemoteGameConsumer(AsyncWebsocketConsumer):

    # list of players in the waiting group
    waiting_room = []

    async def add_to_waiting_room(self, player):
        # send "waiting" state to the player
        await player.send({
            'type': 'state',
            'state': "waiting",
            'p1_name': player.get_user().username,
            'p2_name': "...",
        })
        # check if another player is already waiting
        if len(RemoteGameConsumer.waiting_room) >= 1:
            player1 = RemoteGameConsumer.waiting_room[0]
            RemoteGameConsumer.waiting_room.pop(0)
            game_group = await GameHandler.create(player1, player)
            asyncio.ensure_future(game_group.start_game())
        else:
            RemoteGameConsumer.waiting_room.append(player)
    
    async def connect(self):
        await self.accept()
        if self.scope["user"].is_authenticated:
            if Player.get_channel_by_user(self.scope["user"]) != None:
                print(f"User {self.scope['user'].id} is already connected.")
                await self.send(text_data=json.dumps({
                    'type': 'message',
                    'message': 'You are already connected with another device.',
                }))
                await self.close() # later maybe don't close the connection, but ask the user if he wants to disconnect the other device
                return
            # create new player object
            player = Player(self.scope["user"], self.channel_name)
            await player.send({
                'type': 'message',
                'message': 'Welcome!',
            })
            await player.send({
                'type': 'state',
                'state': "menu",
                'p1_name': "",
                'p2_name': "",
            })
            print(f"{self.scope['user'].username} connected to game-websocket.")
    

    # DIESE RECEIVE FUNKTION MUSS DEFINITIV NOCH ÜBERARBEITET WERDEN !
    # ERST DATENTYP CHECKEN UND DANN GUCKEN OB IM GAME UND SO... SONDT SCHNELL ERROR!
    # WENN MENU_DATA KOMMT UND SPIELER IN GAME SOLLTE NICHTS PASSIEREN....
    async def receive(self, text_data):
        try:
            player = Player.get_player_by_channel(self.channel_name)
            # check if player is in a game group
            if player.get_game_group() != None:
                # get the game data
                game_data = json.loads(text_data)
                # update the paddle
                player.get_game_group().update_paddle(player, game_data.get('key'), game_data.get('type'))
            else:
                # get the menu data
                menu_data = json.loads(text_data)
                # check if the user wants to start a game
                if menu_data.get('type') == 'start_game':
                    await self.add_to_waiting_room(player)
                else:
                    print(f"Received invalid JSON file: {menu_data}")
        except json.JSONDecodeError:
            print(f"Received invalid JSON file")
        
    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            player = Player.get_player_by_channel(self.channel_name)
            if player != None:
                # Stop the game if the user is in a game group (LATER CHANGE THIS TO WAIT A FEW SECONDS AND CHECK IF THE USER RECONNECTS)
                if player.get_game_group() != None:
                    print(f"Stopping game group: {player.get_game_group()}")
                    player.get_game_group().stop_game()
                # remove player from waiting room list if in there
                if player in RemoteGameConsumer.waiting_room:
                    RemoteGameConsumer.waiting_room.remove(player)
                # remove player from list of all players
                Player.all_players.remove(Player.get_player_by_channel(self.channel_name))
                print(f"{self.scope['user'].username} disconnected from game-websocket.")


    #########################
    # group message handler #
    #########################
                            
    async def message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
        }))

    async def game_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'state': event['state'],
            'high_score': event['high_score'],
        }))
    
    async def state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'state',
            'state': event['state'], # "playing", "waiting", "finished" ...
            'p1_name': event['p1_name'],
            'p2_name': event['p2_name'],
        }))
    
    async def winner(self, event):
        await self.send(text_data=json.dumps({
            'type': 'winner',
        }))
    
    async def loser(self, event):
        await self.send(text_data=json.dumps({
            'type': 'loser',
        }))

