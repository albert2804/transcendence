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

#2FA stuff

from django.conf import settings
from django_otp.plugins.otp_totp.models import TOTPDevice
import datetime
import pyotp
import qrcode
import base64
import binascii
import jwt
from io import BytesIO



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
			'is_42_login': request.user.is_42_login,
            }, status=200)
    else:
        return JsonResponse({'authenticated': False}, status=200)

# check if user exists (username)
# 200: user exists / does not exist
# 400: invalid request
#
# As API request call:
# curl -k -X GET 'https://localhost/endpoint/api/userexists?username=<USERNAME>'
#
def userexists(request):
	if request.method == 'GET':
		username = request.GET.get('username')
		if username:
			try:
				user = CustomUser.objects.get(username=username)
				return JsonResponse({'exists': True}, status=200)
			except CustomUser.DoesNotExist:
				return JsonResponse({'exists': False}, status=200)
		else:
			return JsonResponse({'error': 'No username provided'}, status=401)
	return JsonResponse({'error': 'Invalid request'}, status=402)


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
            token = data.get('token')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Something went wrong'}, status=400)
        # check if user is already logged in
        if request.user.is_authenticated:
            return JsonResponse({
                'message': 'You are already logged in',
                }, status=200)
        # try to authenticate and login user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # check if the user has 2FA enabled
            if user.enabled_2fa:
                try:
                    device = TOTPDevice.objects.get(user=user)
                    # If they do, verify the token
                    if token is None or not device.verify_token(token):
                        return JsonResponse({'error': 'Invalid 2FA token'}, status=403)
                except TOTPDevice.DoesNotExist:
                    # If they don't have 2FA enabled, we don't need to check the token
                    pass
            login(request, user)
            user_id = user.id
             # Create JWT token
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow()
            }
            jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            response = JsonResponse({
                'message': 'Successfully logged in as ' + request.user.username,
                'username': request.user.username,
                'userid': user_id
                }, status=200)
            response.set_cookie('jwt_token', jwt_token, httponly=True, secure=True, samesite='Strict')
            return response
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
        # form = CustomUserCreationForm(request.POST)
        data = json.loads(request.body.decode('utf-8'))
        form = CustomUserCreationForm(data)
        if form.is_valid():
            # save user to database and login
            user_stats = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                user_id = user.id
                return JsonResponse({
                    'message': 'Successfully registered as ' + request.user.username,
                    'username': request.user.username,
                    'userid': user_id,
                    }, status=200)
            else:
                return JsonResponse({'error': 'Something went wrong'}, status=400)
        else:
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

# get qr code for 2FA

def qr_code(request):
    user = request.user
    if user.enabled_2fa:
        return JsonResponse({'error': '2FA is already enabled for this user'}, status=400)

    # Check if an unconfirmed TOTP device already exists for the user
    totp_device = TOTPDevice.objects.filter(user=user, confirmed=False).first()

    if not totp_device:
        # Generate a random secret key
        secret_key_base32 = pyotp.random_base32()
        secret_key_hex = binascii.hexlify(base64.b32decode(secret_key_base32)).decode()

        # Create a new TOTP device for the user
        totp_device = TOTPDevice.objects.create(user=user, confirmed=False, key=secret_key_hex)
    else:
        # If a TOTP device already exists, use its key to instantiate a TOTP object
        secret_key_base32 = base64.b32encode(binascii.unhexlify(totp_device.key)).decode()

    # Instantiate a TOTP object
    totp = pyotp.TOTP(secret_key_base32)

    # Generate a provisioning URI for the TOTP device
    provisioning_uri = totp.provisioning_uri(name=user.username, issuer_name='42 Pong')

    # Generate a QR code from the provisioning URI
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(provisioning_uri)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered)

    # Encode the QR code image in base64 and return it in the response
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()

    return JsonResponse({'qr_code': qr_code_base64})


# enable 2FA for user
def enable_2fa(request, *args, **kwargs):
    user = request.user
    if user.is_42_login:
        return JsonResponse({'error': '42 users cannot enable 2FA'}, status=200)
    if user.enabled_2fa or TOTPDevice.objects.filter(user=user, confirmed=True).exists():
        return JsonResponse({'error': '2FA is already enabled for this user'}, status=200)
    data = json.loads(request.body)
    code = data.get('code')

    # Get the unconfirmed TOTP device for the user
    totp_device = TOTPDevice.objects.filter(user=user, confirmed=False).first()

    if not totp_device:
        return JsonResponse({'error': 'No TOTP device found for this user'}, status=200)

    # Convert the binary key to a base32-encoded string
    bin_key_base32 = base64.b32encode(binascii.unhexlify(totp_device.key)).decode()

    # Verify the code
    totp = pyotp.TOTP(bin_key_base32)
    if totp.verify(code):
        # If the code is valid, confirm the TOTP device
        totp_device.confirmed = True
        totp_device.save()
        user.enabled_2fa = True
        user.save()
        return JsonResponse({'success': '2FA enabled successfully'})
    else:
        return JsonResponse({'error': 'Invalid or expired code'}, status=200)


def get_2fa_status(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                return JsonResponse({'enabled_2fa': user.enabled_2fa})
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            try:
                user = request.user
                if not request.user.is_authenticated:
                    return JsonResponse({'message': 'Need to be logged in to check 2FA status.'}, status=200)
                return JsonResponse({'enabled_2fa': user.enabled_2fa})
            except:
                return JsonResponse({'error': 'No username provided and not logged in'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def disable_2fa(request, *args, **kwargs):
    user = request.user
    if not user.enabled_2fa or not TOTPDevice.objects.filter(user=user, confirmed=True).exists():
        return JsonResponse({'error': '2FA is not enabled for this user'}, status=400)

    # Get the confirmed TOTP device for the user
    totp_device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

    if not totp_device:
        return JsonResponse({'error': 'No TOTP device found for this user'}, status=400)

    # Delete the TOTP device
    totp_device.delete()

    # Disable 2FA for the user
    user.enabled_2fa = False
    user.save()

    return JsonResponse({'success': '2FA disabled successfully'})

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
