from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
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

# Set csrf token cookie
# get_token() is a django function that sets a csrf token cookie in the clients browser
# This gets called automatically from Index.vue
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
        return JsonResponse({'authenticated': True}, status=200)
    else:
        return JsonResponse({'authenticated': False}, status=200)

# userlogin
# 400: invalid json data
# 200: user is authenticated
# 401: user is not authenticated
def userlogin(request):
    if request.method == 'POST':
        # validate json data
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        # check if user is already logged in
        if request.user.is_authenticated:
            return JsonResponse({'message': 'You are already logged in'}, status=200)
        # try to authenticate and login user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Successfully logged in'}, status=200)
    return JsonResponse({'error': 'Invalid credentials'}, status=401)

# userlogout
# 200: user logged out
def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'message': 'Successfully logged out'}, status=200)
    return JsonResponse({'message': 'You are already logged out'}, status=200)

