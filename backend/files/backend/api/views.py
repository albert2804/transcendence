from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
import json

# Set csrf token cookie
# get_token() is a django function that sets a csrf token cookie in the clients browser
# This gets called automatically from Index.vue
def get_csrf(request):
    get_token(request)
    return JsonResponse({'csrfToken': get_token(request)})

# application/json
def getTestJsonData(request):
    test = {'message':"hello world", 'city': "Heilbronn", 'school': 42}
    return JsonResponse(test)

# text/plain or text/html
def getTestTextData(request):
    return HttpResponse("Hello World")

# get auth status of user
def get_auth_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True})
    else:
        return JsonResponse({'authenticated': False})

# login user
def userlogin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'authenticated': False, 'error': 'Invalid JSON data'})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'authenticated': True})
    return JsonResponse({'authenticated': False})
