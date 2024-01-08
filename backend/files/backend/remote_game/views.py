# remote_game/views.py

from django.shortcuts import render
from django.http import JsonResponse

# In-memory game state (not recommended for production)
game_state = {
    'ball_x': 400,
    'ball_y': 200,
    'paddle_left_y': 0.0,
    'paddle_right_y': 0.0,
}

game_parameters = {
    'initalSpeed': 3
}

def update_game_state(request):
    global game_state

    # Update game state based on player input or other logic
    # For simplicity, this is just an example
    game_state['ball_x'] += 1.0
    game_state['ball_y'] += 1.0

    # Return the updated game state as JSON
    return JsonResponse(game_state)
