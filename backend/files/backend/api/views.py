from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
from users.models import Statistics
from .forms import CustomUserCreationForm
from django.middleware.csrf import get_token
from django.db import IntegrityError
import json


################
### EXAMPLES ###
################

# application/json
def getTestJsonData(request):
    test = {'message':"hello world", 'city': "Heilbronn", 'school': 42}
    return JsonResponse(test)

# text/plain or text/html
def getTestTextData(request):
    return HttpResponse("Hello World")


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
            # 'username': request.user.username,
            }, status=200)
    else:
        return JsonResponse({'authenticated': False}, status=200)

# login user
# 400: invalid json data
# 200: user is authenticated
# 403: user is not authenticated
def userlogin(request):
    if request.method == 'POST':
        # validate json data
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
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
            login(request, user)
            user_id = user.id
            return JsonResponse({
                'message': 'Successfully logged in as ' + request.user.username,
                'userid': user_id,
                }, status=200)
    return JsonResponse({'error': 'Invalid credentials'}, status=403)

# logout user
# 200: user logged out
def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': 'Successfully logged out'}, status=200)
    return JsonResponse({'message': 'You are already logged out'}, status=200)

# register user
# 200: user registered
# 400: an error occured
# 403: invalid credentials
def userregister(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        # check input with CustomUserCreationForm
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # save user to database and login
            user_stats = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user_id = user.id
                Statistics.objects.create(user=user_stats)
                return JsonResponse({
                    'message': 'Successfully registered as ' + request.user.username,
                    'userid': user_id,
                    }, status=200)
            else:
                return JsonResponse({'error': 'Something went wrong'}, status=400)
        else:
            # print(form.errors)
            # check if username already exists
            if CustomUser.objects.filter(username=request.POST['username']).exists():
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

