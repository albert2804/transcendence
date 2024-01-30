from .gameHandler import GameHandler
# from .consumers import RemoteGameConsumer
from channels.layers import get_channel_layer

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
    
    async def send_state(self):
        from .consumers import RemoteGameConsumer
        # check if playing
        if self.game_group != None:
            group = GameHandler.get_game_group_by_name(self.game_group)
            print("send playing state")
            await self.send({
                'type': 'state',
                'state': "playing",
                'p1_name': group.player1.get_user().username,
                'p2_name': group.player2.get_user().username,
            })
        # check if in waiting room
        elif self in RemoteGameConsumer.waiting_room:
            print("send waiting state")
            await self.send({
                'type': 'state',
                'state': "waiting",
                'p1_name': self.get_user().username,
                'p2_name': "...",
            })
        # else send menu state
        else:
            print("send menu state")
            await self.send({
                'type': 'state',
                'state': "menu",
                'p1_name': "",
                'p2_name': "",
            })
        
                
    
    async def change_channel(self, new_channel):
        # send "other_device" state to the old channel
        await self.send({
            'type': 'state',
            'state': "other_device",
            'p1_name': "",
            'p2_name': "",
        })
        print(f"Player {self.user.username} changed channel from {self.channel} to {new_channel}")
        if self.game_group != None:
            await self.channel_layer.group_discard(self.game_group, self.channel)
            await self.channel_layer.group_add(self.game_group, new_channel)
        self.channel = new_channel
        # send actual state to the new channel
        await self.send_state()
    
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
        return GameHandler.get_game_group_by_name(self.game_group)
    
    async def send(self, message):
        await self.channel_layer.send(self.channel, message)
