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
#   "password1": "<YOUR PASSWORD>",
#   "password2": "<YOUR PASSWORD>"
# }'
# 
def userregister(request):
	if request.user.is_authenticated:
		logout(request)
	if request.method == 'POST':
		# check input with CustomUserCreationForm
		# form = CustomUserCreationForm(request.POST)
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
	return JsonResponse({'error': 'Something went wrong'}, status=400)


######################
### GAME FUNCTIONS ###
######################

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

#####################
### FRIEND SYSTEM ###
#####################

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
				channel_layer = get_channel_layer()
				async_to_sync(channel_layer.group_send)(f"chat_{request.user.id}", {
					'type': 'handle_friend_command',
					'receiver_id': friend.id,
				})
				return JsonResponse({'message': 'success'}, status=200)
			else:
				return JsonResponse({'error': 'Friend not specified'}, status=400)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Something went wrong'}, status=400)
	return JsonResponse({'error': 'Invalid request'}, status=400)

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
				channel_layer = get_channel_layer()
				async_to_sync(channel_layer.group_send)(f"chat_{request.user.id}", {
					'type': 'handle_unfriend_command',
					'receiver_id': friend.id,
					'remove': True,
				})
				return JsonResponse({'message': 'success'}, status=200)
			else:
				return JsonResponse({'error': 'Friend not specified'}, status=400)
		except json.JSONDecodeError:
			return JsonResponse({'error': 'Something went wrong'}, status=400)