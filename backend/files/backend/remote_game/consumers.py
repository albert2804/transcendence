from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import models
from django.contrib.auth import get_user_model
import json
import random
import asyncio
from .utils import PongGame

# TODO: send user object or id instead of p1_channel and p2_channel to GameGroup.
#       this way the game can be continued if the user disconnects and reconnects
#       (the user object is still the same, but the channel name changes)
#       -> we can still send messages to the user with his private channel name (f"game_user_{user.id}")
#       -> also we don't need to use the "channel_to_user" from RemoteGameConsumer here in GameGroup !

# TODO: In Frontend: if websocket connection is closed -> show message "Connection lost. Please reload the page."
#       hmm maybe send a disconnection code to the frontend and show a message there (for example if the user is already connected with another device)
#       google about close_code for the disconnect function ;)

class GameGroup:
    def __init__(self, p1_channel, p2_channel, game_group, channel_layer):
        self.p1_channel = p1_channel
        self.p2_channel = p2_channel
        self.game_group = game_group
        self.game = PongGame()
        self.channel_layer = channel_layer

    async def start_game(self):
        print(f"Starting game ({self.game_group}).")
        # send info, that game is starting
        await self.channel_layer.group_send(
            self.game_group,
            {
                'type': 'state',
                'state': "playing",
                'p1_name': await database_sync_to_async(lambda: get_user_model().objects.get(id=int(RemoteGameConsumer.channel_to_user[self.p1_channel].id)).username)(),
                'p2_name': await database_sync_to_async(lambda: get_user_model().objects.get(id=int(RemoteGameConsumer.channel_to_user[self.p2_channel].id)).username)(),
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
            await self.channel_layer.group_send(
                f"game_user_{RemoteGameConsumer.channel_to_user[self.p1_channel].id}",
                {
                    'type': 'winner',
                }
            )
            await self.channel_layer.group_send(
                f"game_user_{RemoteGameConsumer.channel_to_user[self.p2_channel].id}",
                {
                    'type': 'loser',
                }
            )
        elif (self.game.winner == 2):
            await self.channel_layer.group_send(
                f"game_user_{RemoteGameConsumer.channel_to_user[self.p1_channel].id}",
                {
                    'type': 'loser',
                }
            )
            await self.channel_layer.group_send(
                f"game_user_{RemoteGameConsumer.channel_to_user[self.p2_channel].id}",
                {
                    'type': 'winner',
                }
            )
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
        #### THIS PART NEEDS HIS OWN FUNCTION ##############
        # remove game group from maps if still there
        if self.game_group in RemoteGameConsumer.game_groups:
            del RemoteGameConsumer.game_groups[self.game_group]
            del RemoteGameConsumer.channel_to_game_group[self.p1_channel]
            del RemoteGameConsumer.channel_to_game_group[self.p2_channel]
        # remove channels from game group
        await self.channel_layer.group_discard(self.game_group, self.p1_channel)
        await self.channel_layer.group_discard(self.game_group, self.p2_channel)
        ####################################################

    
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

    # maps of connected channels
    # this map is needed later to know which user is connected to which channel
    channel_to_user = {}    # key: channel_name,    value: user object

    # channel_name to game_group_name (one entry for each player who is in a game group)
    channel_to_game_group = {}
    # INFO: der game_group_name ist gleichzeitig der channel_name der game group

    # map of game groups (game_group_name: GameGroup)
    game_groups = {}
    
    async def add_to_waiting_group(self, channel_name):
        # send "waiting" state to the player
        # username = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(RemoteGameConsumer.channel_to_user[channel_name])).username)()
        username = await database_sync_to_async(lambda: get_user_model().objects.get(id=int(self.scope["user"].id)).username)()
        await self.channel_layer.group_send(
            # f"game_user_{self.channel_to_user[channel_name]}",
            f"game_user_{self.scope['user'].id}",
            {
                'type': 'state',
                'state': "waiting",
                'p1_name': username,
                'p2_name': "...",
            }
        )
        # add consumer to the group of waiting players
        await self.channel_layer.group_add("waiting", channel_name)
        # check if there is another player waiting
        if len(self.channel_layer.groups["waiting"]) >= 2:
            new_group_name = f"game_group_{random.randint(0, 1000000)}" # enough randomness to avoid collisions ??
            waiting_channel_ids = list(self.channel_layer.groups["waiting"])
            # check again if there are still enough players waiting (because of asyncronous code)
            if len(waiting_channel_ids) >= 2:
                # move players from waiting group to new game group
                await self.channel_layer.group_add(new_group_name, waiting_channel_ids[0])
                await self.channel_layer.group_discard("waiting", waiting_channel_ids[0])
                await self.channel_layer.group_add(new_group_name, waiting_channel_ids[1])
                await self.channel_layer.group_discard("waiting", waiting_channel_ids[1])
                # create new game group
                RemoteGameConsumer.game_groups[new_group_name] = GameGroup(waiting_channel_ids[0], waiting_channel_ids[1], new_group_name, self.channel_layer)
                # add players to the game group
                RemoteGameConsumer.channel_to_game_group[waiting_channel_ids[0]] = new_group_name
                RemoteGameConsumer.channel_to_game_group[waiting_channel_ids[1]] = new_group_name
                # start the game in the game group in a new thread
                asyncio.ensure_future(RemoteGameConsumer.game_groups[new_group_name].start_game())
            else:
                # remove the new created group
                del self.channel_layer.groups[new_group_name]
    
    async def group_exists(self, group_name):
        return bool(self.channel_layer.groups.get(group_name, False))
    
    async def connect(self):
        await self.accept()
        if self.scope["user"].is_authenticated:
            # add user to the channel_to_user map
            RemoteGameConsumer.channel_to_user[self.channel_name] = self.scope["user"]
            # check if user is already connected
            if await self.group_exists(f"game_user_{self.scope['user'].id}"):
                print(f"User {self.scope['user'].id} is already connected.")
                await self.send(text_data=json.dumps({
                    'type': 'message',
                    'message': 'You are already connected with another device.',
                }))
                await self.close()
                return
            #  add user to his own group / create group for the user
            await self.channel_layer.group_add(
                f"game_user_{self.scope['user'].id}",
                self.channel_name
            )
            await self.send(text_data=json.dumps({
                'type': 'message',
                'message': 'Welcome!',
            }))
            await self.channel_layer.group_send(
                f"game_user_{self.scope['user'].id}",
                {
                    'type': 'state',
                    'state': "menu",
                    'p1_name': "",
                    'p2_name': "",
                }
            )
            print(f"User {self.scope['user']} connected.")
    

    # DIESE RECEIVE FUNKTION MUSS DEFINITIV NOCH ÜBERARBEITET WERDEN !
    # ERST DATENTYP CHECKEN UND DANN GUCKEN OB IM GAME UND SO... SONDT SCHNELL ERROR!
    # WENN MENU_DATA KOMMT UND SPIELER IN GAME SOLLTE NICHTS PASSIEREN....
    async def receive(self, text_data):
        try:
            # check if user is in a game group
            if self.channel_name in RemoteGameConsumer.channel_to_game_group:
                # get the game data
                game_data = json.loads(text_data)
                # get the game group
                game_group_name = RemoteGameConsumer.channel_to_game_group[self.channel_name]
                game_group = RemoteGameConsumer.game_groups[game_group_name]
                # update the paddle
                game_group.update_paddle(self.channel_name, game_data.get('key'), game_data.get('type'))
            else:
                # get the menu data
                menu_data = json.loads(text_data)
                # check if the user wants to start a game
                if menu_data.get('type') == 'start_game':
                    await self.add_to_waiting_group(self.channel_name)
                else:
                    print(f"Received invalid JSON file: {menu_data}")
        except json.JSONDecodeError:
            print(f"Received invalid JSON file")
        
    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            # remove user from the channel_to_user map
            if self.channel_name in RemoteGameConsumer.channel_to_user:
                del RemoteGameConsumer.channel_to_user[self.channel_name]
            # remove user from his own group
            await self.channel_layer.group_discard(
                f"game_user_{self.scope['user'].id}",
                self.channel_name
            )
            # check if user group still exists (if not, the user disconnected with all his devices)
            if not await self.group_exists(f"game_user_{self.scope['user'].id}"):
                print(f"User {self.scope['user'].id} disconnected.")
            # remove user from the waiting group
            await self.channel_layer.group_discard("waiting", self.channel_name)
            # check if user is in a game group
            if self.channel_name in RemoteGameConsumer.channel_to_game_group:
                RemoteGameConsumer.game_groups[RemoteGameConsumer.channel_to_game_group[self.channel_name]].stop_game()



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

