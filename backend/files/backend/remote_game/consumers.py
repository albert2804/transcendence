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


class Player:
    # static variable to store all instances of this class
    all_players = []

    # STATIC METHODS

    def get_player_by_channel(channel):
        for player in Player.all_players:
            if player.get_channel() == channel:
                return player
        return None

    def get_channel_by_user(user):
        for player in Player.all_players:
            if player.get_user() == user:
                return player.get_channel()
        return None
    
    # INSTANCE METHODS

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
    
    async def remove_from_game_group(self):
        await self.channel_layer.group_discard(
            self.game_group,
            self.channel
        )
        self.game_group = None
    
    def get_game_group(self):
        return GameGroup.get_game_group_by_name(self.game_group)
    
    async def send(self, message):
        await self.channel_layer.send(self.channel, message)

    


class GameGroup:

    # static variable to store all instances of this class
    all_game_groups = {}

    # STATIC METHODS

    def get_game_group_by_name(game_group_name):
        return GameGroup.all_game_groups.get(game_group_name, None)


    # INSTANCE METHODS

    def __init__(self, p1_channel, p2_channel, game_group):
        self.p1_channel = p1_channel
        self.p2_channel = p2_channel
        self.game_group = game_group
        self.game = PongGame()
        self.channel_layer = get_channel_layer()
        GameGroup.all_game_groups[game_group] = self

    async def start_game(self):
        print(f"Starting game ({self.game_group}).")
        # send info, that game is starting
        await self.channel_layer.group_send(
            self.game_group,
            {
                'type': 'state',
                'state': "playing",
                'p1_name': Player.get_player_by_channel(self.p1_channel).get_user().username,
                'p2_name': Player.get_player_by_channel(self.p2_channel).get_user().username,
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
            await Player.get_player_by_channel(self.p1_channel).send({
                'type': 'winner',
            })
            await Player.get_player_by_channel(self.p2_channel).send({
                'type': 'loser',
            })
        elif (self.game.winner == 2):
            await Player.get_player_by_channel(self.p1_channel).send({
                'type': 'loser',
            })
            await Player.get_player_by_channel(self.p2_channel).send({
                'type': 'winner',
            })
        # wait 5 seconds
        await asyncio.sleep(5)
        print(f"Game ({self.game_group}) finished.")
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
        del GameGroup.all_game_groups[self.game_group]
        del self

    
    def stop_game(self):
        print(f"Stopping game ({self.game_group}).")
        self.game.isGameExited = True
    
    def update_paddle(self, channel_name, key, type):
        if channel_name == self.p1_channel:
            if type == 'key_pressed':
                if key == 'ArrowUp':
                    self.game.leftPaddle['dy'] = -2
                elif key == 'ArrowDown':
                    self.game.leftPaddle['dy'] = 2
            elif type == 'key_released':
                if key in ['ArrowDown', 'ArrowUp']:
                    self.game.leftPaddle['dy'] = 0
        elif channel_name == self.p2_channel:
            if type == 'key_pressed':
                if key == 'ArrowUp':
                    self.game.rightPaddle['dy'] = -2
                elif key == 'ArrowDown':
                    self.game.rightPaddle['dy'] = 2
            elif type == 'key_released':
                if key in ['ArrowDown', 'ArrowUp']:
                    self.game.rightPaddle['dy'] = 0
        else:
            print(f"Unknown channel name: {channel_name}")
    
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
        # add player to the waiting room
        RemoteGameConsumer.waiting_room.append(player)
        # check if there is another player waiting
        if len(RemoteGameConsumer.waiting_room) >= 2:
            new_group_name = f"game_group_{random.randint(0, 1000000)}"
            # remove the first two players from the waiting room
            player1 = RemoteGameConsumer.waiting_room[0]
            await player1.add_to_game_group(new_group_name) # move this to the GameGroup init function
            RemoteGameConsumer.waiting_room.pop(0)
            player2 = RemoteGameConsumer.waiting_room[0]
            await player2.add_to_game_group(new_group_name) # move this to the GameGroup init function
            RemoteGameConsumer.waiting_room.pop(0)
            # create new game group object
            game_group = GameGroup(player1.get_channel(), player2.get_channel(), new_group_name) # CHANGE HERE !!!!!!!!!!!!
            # start the game in the game group in a new thread
            asyncio.ensure_future(game_group.start_game())
            # print("XXXXXXXXX")
    
    async def connect(self):
        await self.accept()
        if self.scope["user"].is_authenticated:
            if Player.get_channel_by_user(self.scope["user"]) != None:
                print(f"User {self.scope['user'].id} is already connected.")
                await self.send(text_data=json.dumps({
                    'type': 'message',
                    'message': 'You are already connected with another device.',
                }))
                await self.close()
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
            print(f"User {self.scope['user']} connected.")
    

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
                player.get_game_group().update_paddle(self.channel_name, game_data.get('key'), game_data.get('type'))
            else:
                # get the menu data
                menu_data = json.loads(text_data)
                # check if the user wants to start a game
                if menu_data.get('type') == 'start_game':
                    # await self.add_to_waiting_group(self.channel_name)
                    await self.add_to_waiting_room(player)
                else:
                    print(f"Received invalid JSON file: {menu_data}")
        except json.JSONDecodeError:
            print(f"Received invalid JSON file")
        
    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            # ger player object
            player = Player.get_player_by_channel(self.channel_name)
            # if Player.get_channel_by_user(self.scope["user"]) != None:
            if player != None:
                # Stop the game if the user is in a game group (LATER CHANGE THIS TO WAIT A FEW SECONDS AND CHECK IF THE USER RECONNECTS)
                # if Player.get_player_by_channel(self.channel_name).get_game_group() != None:
                #     Player.get_player_by_channel(self.channel_name).get_game_group().stop_game()
                if player.get_game_group() != None:
                    print(f"Stopping game group: {player.get_game_group()}")
                    player.get_game_group().stop_game()
                
                # remove player from waiting room if in there (the list)
                # if Player.get_player_by_channel(self.channel_name) in RemoteGameConsumer.waiting_room:
                #     RemoteGameConsumer.waiting_room.remove(Player.get_player_by_channel(self.channel_name))
                if player in RemoteGameConsumer.waiting_room:
                    print(f"Removing player from waiting room.")
                    RemoteGameConsumer.waiting_room.remove(player)

                # remove player from list of all players
                Player.all_players.remove(Player.get_player_by_channel(self.channel_name))
                print(f"User {self.scope['user'].id} disconnected.")


                # TODO:
                # maybe implement a static function in the Player class to remove a player from the list of all players
                # so we can stop the game automatically if the user disconnects
                # Other idea: do not delete the player from the list of all players directly, but "pause" the game and wait for the user to reconnect


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

