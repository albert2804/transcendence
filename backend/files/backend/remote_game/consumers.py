# remote_game/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import models
from django.contrib.auth import get_user_model
import json
import random
import asyncio
from .utils import PongGame

class RemoteGameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = PongGame()

    async def connect(self):
        await self.accept()
        print(f"upgrade to websocket accepted")
        # Start sending periodic game state updates
        asyncio.ensure_future(self.send_periodic_updates())
        print(f"periodic updates started")
        User = get_user_model()
        print(f"Welcome ", User)
        # player = User.objects.get(id=int())
        # print(f"Welcome ", player)

    async def disconnect(self, close_code):
        print(f"websocket connection closed")
        pass

    async def receive(self, text_data):

        try:    
            game_data = json.loads(text_data)
            key_pressed = game_data.get('key_pressed')
            key_released = game_data.get('key_released')

            # Perform actions based on the pressed key
            if key_pressed == 'ArrowUp':
                # print(f"key pressed: {key_pressed}")
                self.game.rightPaddle['dy'] = -2
                # print(f"paddle", self.game.rightPaddle['y'])
            elif key_pressed == 'ArrowDown':
                # print(f"key pressed: {key_pressed}")
                self.game.rightPaddle['dy'] = 2
                # print(f"paddle", self.game.rightPaddle['y'])
            elif key_released in ['ArrowDown', 'ArrowUp']:
                # print(f"key released: {key_released}")
                self.game.rightPaddle['dy'] = 0
                # print(f"paddle", self.game.rightPaddle['y'])
            elif key_pressed == 'Escape':
                self.game.isGameExited=True

            if self.game.isGameExited :
                    self.close()

        except json.JSONDecodeError:
            print(f"Received invalid JSON file: {game_data}")

                
    async def send_game_state(self):
        state = {
            'ball': {
                'x': self.game.ball['x'],
                'y': self.game.ball['y'],
                'radius': self.game.ball['radius'],
            },
            'leftPaddle': {
                'x': self.game.leftPaddle['x'],
                'y': self.game.leftPaddle['y'],
                'width': self.game.leftPaddle['width'],
                'height': self.game.leftPaddle['height'],
            },
            'rightPaddle': {
                'x': self.game.rightPaddle['x'],
                'y': self.game.rightPaddle['y'],
                'width': self.game.rightPaddle['width'],
                'height': self.game.rightPaddle['height'],
            },
        }
        high_score = {
            'numberOfHitsP1': self.game.numberOfHitsP1,
            'numberOfHitsP2': self.game.numberOfHitsP2,
        }
        await self.send(text_data=json.dumps({
            'type': 'game_update',
            'state': state,
            'high_score': high_score,
        }))

    async def send_periodic_updates(self):
        while not self.game.isGameExited:
            # Update game state periodically
            self.game.game_loop()
            await self.send_game_state()

            # Adjust the sleep duration based on your desired update frequency
            await asyncio.sleep(0.003)  # Send updates every 0.002 second for a smooth UX