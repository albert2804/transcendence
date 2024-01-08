# remote_game/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import random
import asyncio

class RemoteGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print(f"upgrade to websocket accepted")
        # Start sending periodic game state updates
        asyncio.ensure_future(self.send_periodic_updates())
        print(f"periodic updates started")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        key_pressed = data.get('key_pressed')

        # Perform actions based on the pressed key
        if key_pressed == 'w':
            print(f"key pressed: {key_pressed}")
            # Your action here

        # Add more conditions for other keys as needed
        # send_game_state()

    async def send_game_state(self, event):
        # Send updated game state to the client
        await self.send(text_data=json.dumps({
            'type': 'game_state',
            'state': event['state'],
        }))

    async def send_periodic_updates(self):
        while True:
            # Update game state periodically (replace with your game logic)
            updated_state = {
                'ball_x': 123.45,
                'ball_y': 67.89,
                'paddle_left_y': 12.34,
                'paddle_right_y': 56.78,
            }

            # Call send_game_state to send the updated state to clients
            await self.send_game_state({'state': updated_state})
            print(f"periodic update submitted")
            print(f"state:", updated_state['ball_x'])

            # Adjust the sleep duration based on your desired update frequency
            await asyncio.sleep(1)  # Send updates every 1 second (adjust as needed)