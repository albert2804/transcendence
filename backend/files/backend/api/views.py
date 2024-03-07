from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.middleware.csrf import get_token
from django.db import IntegrityError
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from remote_game.consumers import RemoteGameConsumer
from chat.consumers import ChatConsumer
from remote_game.player import Player


################
### SECURITY ###
################

# set csrf token cookie
# you need to send your csrf token with every POST request (e.g. login, register)
# get_token() is a django function that sets a csrf token cookie in the clients browser
# This gets called from onMounted() in Index.vue !
def get_csrf(request):
	get_token(request)
	return JsonResponse({'csrfToken': get_token(request)})


###########################
### USER AUTHENTICATION ###
###########################

# get auth status of user
# this is called from Index.vue to check if the user is authenticated
# returns a json object with a boolean value that indicates if the user is authenticated
# 200: successfull request
def get_auth_status(request):
	if request.user.is_authenticated:
		return JsonResponse({
			'authenticated': True,
			'user_id': request.user.id,
			'username': request.user.username,
			}, status=200)
	else:
		return JsonResponse({'authenticated': False}, status=200)


# login user
# 400: invalid json data or request
# 200: user is authenticated
# 403: user is not authenticated
# 
# As API request call:
# curl -k -X POST 'https://localhost/endpoint/api/userlogin' \
# -H 'Content-Type: application/json' \
# -d '{
#   "username": "<YOUR USERNAME>",
#   "password": "<YOUR PASSWORD>"
# }'
# 
def userlogin(request):
	if request.method == 'POST':
		# validate json data
		try:
			data = json.loads(request.body.decode('utf-8'))
			username = data.get('username')
			password = data.get('password')
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Something went wrong'}, status=400)
		# check if user is already logged in and if form valid
		if request.user.is_authenticated:
			return JsonResponse({
				'message': 'You are already logged in',
				}, status=200)
		# try to authenticate and login user
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			user_id = user.id
			return JsonResponse({
				'message': 'Successfully logged in as ' + request.user.username,
				'username': request.user.username,
				'userid': user_id,
				'sessionid': request.session.session_key,
				}, status=200)
		return JsonResponse({'error': 'Invalid credentials'}, status=403)
	return JsonResponse({'error': 'Invalid request'}, status=400)


# logout user
# 200: user logged out
# 
# As API request call:
# curl -k -X POST 'https://localhost/endpoint/api/userlogout' \
# -H 'Authorization: Bearer <YOUR SESSION-ID>' \
# -H 'Content-Type: application/json'
# 
def userlogout(request):
	if request.user.is_authenticated:
		logout(request)
		return JsonResponse({'message': 'Successfully logged out'}, status=200)
	return JsonResponse({'message': 'You are already logged out'}, status=200)


# register user
# 200: user registered
# 400: an error occured
# 403: invalid credentials
# 
# As API request call:
# curl -k -X POST 'https://localhost/endpoint/api/userregister' \
# -H 'Content-Type: application/json' \
# -d '{
#   "username": "<YOUR USERNAME>",
#	"alias": "<YOUR ALIAS>,
#   "password1": "<YOUR PASSWORD>",
#   "password2": "<YOUR PASSWORD>"
# }'
# 
def userregister(request):
	if request.user.is_authenticated:
		logout(request)
	if request.method == 'POST':
		# check input with CustomUserCreationForm
		data = json.loads(request.body.decode('utf-8'))
		# print(data)
		form = CustomUserCreationForm(data)
		if form.is_valid():
			# save user to database and login
			user_stats = form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				user_id = user.id
				return JsonResponse({
					'message': 'Successfully registered as ' + request.user.username,
					'username': request.user.username,
					'userid': user_id,
					}, status=200)
			else:
				return JsonResponse({'error': 'Something went wrong'}, status=400)
		else:
			# print(form.errors)
			# check if username already exists
			if CustomUser.objects.filter(username=data['username']).exists():
				return JsonResponse({'error': 'Username already exists'}, status=403)
			# check form.errors for other username errors
			if 'username' in form.errors:
				return JsonResponse({'error': 'invalid username'}, status=403)
			# check form.errors for password errors
			if 'password1' or 'password2' in form.errors:
				return JsonResponse({'error': 'invalid password'}, status=403)
			# any other errors
			return JsonResponse({'error': 'invalid credentials'}, status=403)
	return JsonResponse({'error': 'Invalid request'}, status=400)


######################
### GAME FUNCTIONS ###
######################

# invite someone to a game
# 200: success
# 400: invalid request
# 403: something went wrong (e.g. user not found)
#
# As API request call:
# This request needs a connected game-consumer (websocket) to work, so its not really useful with curl.
# curl -k -X POST 'https://localhost/endpoint/api/invite_to_game' \
# -H 'Content-Type: application/json' \
# -H 'Authorization: Bearer <YOUR SESSION-ID>' \
# -d '{
#   "receiver": "<RECEIVER_USERNAME>"
# }'
# 
def invite_to_game(request):
	if request.method == 'POST':
		try:
			if not request.user.is_authenticated:
				return JsonResponse({'error': 'You are not logged in'}, status=403)
			data = json.loads(request.body.decode('utf-8'))
			if 'receiver' in data:
				receiver = CustomUser.objects.get(username=data['receiver'])
				if receiver == None:
					return JsonResponse({'error': 'User not found'}, status=403)
				if receiver == request.user:
					return JsonResponse({'error': 'You cannot invite yourself'}, status=403)
				gameconsumer_group_name = 'gameconsumer_' + str(request.user.id)
				if gameconsumer_group_name not in RemoteGameConsumer.all_consumer_groups:
					return JsonResponse({'error': 'You do not have a connected game consumer'}, status=403)
				channel_layer = get_channel_layer()
				async_to_sync(channel_layer.group_send)('gameconsumer_' + str(request.user.id), {
					'type': 'invite_to_game',
					'user_id_1': request.user.id,
					'user_id_2': receiver.id,
				})
				return JsonResponse({'message': 'success'}, status=200)
			else:
				return JsonResponse({'error': 'Receiver not specified'}, status=400)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Something went wrong'}, status=400)
	return JsonResponse({'error': 'Invalid request'}, status=400)


# move the paddel in the active game
# 200: success
# 400: invalid request
# 403: something went wrong (e.g. user not found)
#
# As API request call:
# This request needs a running game for the user.
# This request immitates ArrowUp and ArrowDown key presses to move the paddel in the game.
# So if you play a local game, it will move the paddle of the player that uses the Arrow-Keys for movement.
# Send anything else than 'up' or 'down' as direction to stop the paddel movement.
# curl -k -X POST 'https://localhost/endpoint/api/move_paddle' \
# -H 'Content-Type: application/json' \
# -H 'Authorization: Bearer <YOUR SESSION-ID>' \
# -d '{
#   "direction": "<up or down>"
# }'sw
#
def move_paddle(request):
	if request.method == 'POST':
		try:
			if not request.user.is_authenticated:
				return JsonResponse({'error': 'You are not logged in'}, status=403)
			data = json.loads(request.body.decode('utf-8'))
			if 'direction' in data:
				direction = data['direction']
				gameconsumer_group_name = 'gameconsumer_' + str(request.user.id)
				if gameconsumer_group_name not in RemoteGameConsumer.all_consumer_groups:
					return JsonResponse({'error': 'You do not have a connected game consumer'}, status=403)
				# check if a game is running
				player = Player.get_player_by_user(request.user)
				if player == None or player.game_handler == None:
					return JsonResponse({'error': 'You are not in a game'}, status=403)
				# send move_paddel command to game consumer
				channel_layer = get_channel_layer()
				async_to_sync(channel_layer.group_send)('gameconsumer_' + str(request.user.id), {
					'type': 'move_paddle',
					'direction': direction,
				})
				return JsonResponse({'message': 'success'}, status=200)
			else:
				return JsonResponse({'error': 'Direction not specified'}, status=400)
		except:
			return JsonResponse({'error': 'Something went wrong'}, status=400)
	return JsonResponse({'error': 'Invalid request'}, status=400)


# get the leaderboard
# 200: success
# 400: invalid request
#
# As API request call:
# curl -k -X GET 'https://localhost/endpoint/api/get_leaderboard' \
# -H 'Content-Type: application/json'
#
def get_leaderboard(request):
	if request.method == 'GET':
		# get all users and sort them by mmr in descending order
		users = CustomUser.objects.all()
		users_list = [{ 'username': user.username, 'mmr': user.mmr } for user in users ]
		users_list_sorted = sorted(users_list, key=lambda x: x['mmr'], reverse=True)
		return JsonResponse({ 'leaderboard': users_list_sorted }, status=200)
	return JsonResponse({'error': 'Invalid request'}, status=400)


#####################
### FRIEND SYSTEM ###
#####################

# get friends
# 200: success
# 400: invalid request
# 403: something went wrong (e.g. user not found)
#
# As API request call:
# curl -k -X GET 'https://localhost/endpoint/api/get_friends' \
# -H 'Content-Type: application/json' \
# -H 'Authorization: Bearer <YOUR SESSION-ID>'
#
def get_friends(request):
	if request.method == 'GET':
		if not request.user.is_authenticated:
			return JsonResponse({'error': 'You are not logged in'}, status=403)
		friends = request.user.friends.all()
		friends_list = [{ 'username': friend.username } for friend in friends ]
		return JsonResponse({ 'friends': friends_list }, status=200)
	return JsonResponse({'error': 'Invalid request'}, status=400)


# add friend
# 200: success
# 400: invalid request
# 403: something went wrong (e.g. user not found)
#
# As API request call:
# This request needs a connected chat-consumer (websocket) to work, so its not really useful with curl.
# curl -k -X POST 'https://localhost/endpoint/api/add_friend' \
# -H 'Content-Type: application/json' \
# -H 'Authorization: Bearer <YOUR SESSION-ID>' \
# -d '{
#   "receiver": "<RECEIVER_USERNAME>"
# }'
#
def add_friend(request):
	if request.method == 'POST':
		try:
			if not request.user.is_authenticated:
				return JsonResponse({'error': 'You are not logged in'}, status=403)
			data = json.loads(request.body.decode('utf-8'))
			if 'receiver' in data:
				friend = CustomUser.objects.get(username=data['receiver'])
				if friend == None:
					return JsonResponse({'error': 'User not found'}, status=403)
				if friend == request.user:
					return JsonResponse({'error': 'You cannot add yourself'}, status=403)
				chat_consumer_group_name = 'chat_' + str(request.user.id)
				if chat_consumer_group_name not in ChatConsumer.group_to_channels_mapping:
					return JsonResponse({'error': 'You do not have a connected chat consumer'}, status=403)
				channel_layer = get_channel_layer()
				first_channel = ChatConsumer.group_to_channels_mapping[chat_consumer_group_name][0]
				async_to_sync(channel_layer.send)(first_channel, {
					'type': 'handle_friend_command',
					'receiver_id': friend.id,
				})
				return JsonResponse({'message': 'success'}, status=200)
			else:
				return JsonResponse({'error': 'Friend not specified'}, status=400)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Something went wrong'}, status=400)
	return JsonResponse({'error': 'Invalid request'}, status=400)


# remove friend
# 200: success
# 400: invalid request
# 403: something went wrong (e.g. user not found)
#
# As API request call:
# This request needs a connected chat-consumer (websocket) to work, so its not really useful with curl.
# curl -k -X POST 'https://localhost/endpoint/api/remove_friend' \
# -H 'Content-Type: application/json' \
# -H 'Authorization: Bearer <YOUR SESSION-ID>' \
# -d '{
#   "receiver": "<RECEIVER_USERNAME>"
# }'
#
def remove_friend(request):
	if request.method == 'POST':
		try:
			if not request.user.is_authenticated:
				return JsonResponse({'error': 'You are not logged in'}, status=403)
			data = json.loads(request.body.decode('utf-8'))
			if 'receiver' in data:
				friend = CustomUser.objects.get(username=data['receiver'])
				if friend == None:
					return JsonResponse({'error': 'User not found'}, status=403)
				if friend == request.user:
					return JsonResponse({'error': 'You cannot remove yourself'}, status=403)
				chat_consumer_group_name = 'chat_' + str(request.user.id)
				if chat_consumer_group_name not in ChatConsumer.all_consumer_groups:
					return JsonResponse({'error': 'You do not have a connected chat consumer'}, status=403)
				channel_layer = get_channel_layer()
				first_channel = ChatConsumer.group_to_channels_mapping[chat_consumer_group_name][0]
				async_to_sync(channel_layer.send)(first_channel, {
					'type': 'handle_unfriend_command',
					'receiver_id': friend.id,
					'remove': True,
				})
				return JsonResponse({'message': 'success'}, status=200)
			else:
				return JsonResponse({'error': 'Friend not specified'}, status=400)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Something went wrong'}, status=400)
	return JsonResponse({'error': 'Invalid request'}, status=400)
