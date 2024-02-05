# # remote_game/views.py

# from django.shortcuts import render
# from django.http import JsonResponse
# from .utils import PongGame

# # In-memory game state (not recommended for production)
# game_state = {
#     'ball_x': 400,
#     'ball_y': 200,
#     'paddle_left_y': 0.0,
#     'paddle_right_y': 0.0,
# }

# game_parameters = {
#     'initalSpeed': 3
# }

# def update_game_state(request):
#     global game_state

#     # Update game state based on player input or other logic
#     # For simplicity, this is just an example
#     game_state['ball_x'] += 1.0
#     game_state['ball_y'] += 1.0

#     # Return the updated game state as JSON
#     return JsonResponse(game_state)



# def your_view(request):
#     # Create an instance of the PongGame class
#     pong_game = PongGame()

#     # Update the game state
#     pong_game.update_game()

#     # You can access the updated game state variables like pong_game.ball_x, pong_game.ball_y, etc.

#     # Your view logic here

#     return render(request, 'your_template.html', {'pong_game': pong_game})
