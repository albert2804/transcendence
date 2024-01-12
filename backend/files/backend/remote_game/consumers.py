# remote_game/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
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

    async def disconnect(self, close_code):
        print(f"websocket connection closed")
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        key_pressed = data.get('key_pressed')
        key_released = data.get('key_released')

        # Perform actions based on the pressed key
        if key_pressed == 'ArrowUp':
            print(f"key pressed: {key_pressed}")
            self.game.rightPaddle['dy'] = -5
            print(f"paddle", self.game.rightPaddle['y'])
        elif key_pressed == 'ArrowDown':
            print(f"key pressed: {key_pressed}")
            self.game.rightPaddle['dy'] = 5
            print(f"paddle", self.game.rightPaddle['y'])
        elif key_released in ['ArrowDown', 'ArrowUp']:
            print(f"key released: {key_released}")
            self.game.rightPaddle['dy'] = 0
            print(f"paddle", self.game.rightPaddle['y'])
        elif key_pressed == 'Escape':
            self.game.isGameExited=True

        if self.game.isGameExited :
            self.close()

        # Add more conditions for other keys as needed
        # send_game_state()

    # async def send_game_state(self, event):
    #     # Send updated game state to the client
    #     await self.send(text_data=json.dumps({
    #         'type': 'game_state',
    #         'state': event['state'],
    #     }))
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
            'numberOfWinsP1': self.game.numberOfWinsP1,
            'numberOfWinsP2': self.game.numberOfWinsP2,
        }
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'state': state,
            'high_score': high_score,
        }))

    async def send_periodic_updates(self):
        while not self.game.isGameExited:
            # Update game state periodically
            self.game.game_loop()
            await self.send_game_state()

            # Adjust the sleep duration based on your desired update frequency
            await asyncio.sleep(0.005)  # Send updates every 0.005 second for a smooth UX