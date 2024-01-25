from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
import os
from urllib.parse import quote
from api.models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend

import logging
logger = logging.getLogger(__name__)

tabs = [
    {'name':'home', 'dir':"/endpoint/auth/"},
    {'name':'callback', 'dir':"/endpoint/auth/callback/"},
]


def callback(request):
    code = request.GET.get('code')
    print("CODE: " + code)
    print("URL: " + request.get_full_path())
    state = request.GET.get('state')
    print("STATE: " + state)
    client_id = os.environ.get('42INTRA_CLIENT_ID')
    client_secret = os.environ.get('42INTRA_CLIENT_SECRET')
    url = "https://api.intra.42.fr/oauth/token"
    url += "?grant_type=authorization_code"
    url += "&client_id=" + client_id
    url += "&client_secret=" + client_secret
    url += "&code=" + code
    url += "&state=" + state
    url += "&redirect_uri=" + quote("https://localhost/endpoint/auth/callback", safe='')

    print("URL: " + url)
    response = requests.post(url)
    print(response.json())
    print (response.text)

    token = response.json()['access_token'] 
    print("TOKEN: " + token)

    headers = {'Authorization': f'Bearer {token}'}
    endpoint = "https://api.intra.42.fr/v2/"
    print(endpoint + "me/")
    response = requests.get(endpoint + "me/", headers=headers)

    user_details = ""
    if response.status_code == 200:
        user_details = response.json()
        print(user_details)
    else:
        print(f'Error: {response.status_code}')

    user, created = CustomUser.objects.get_or_create(
        username=user_details['login'] + "_42intra",
        defaults={'email': user_details['email']})
    if created:
        print(f'User {user.username} created')
    else:
        print(f'User {user.username} already exists')

    if user is not None:
        backend = ModelBackend()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        print(f'User {user.username} logged in')
# ...





    # print(f"username: {user_details['login']}")

    return HttpResponse("This is the callback view.\n" + "USERDATA:\n" + "\nURL called: " + json.dumps(user_details))


def home(request):
    context = {
        'tabs':tabs
    }

    return render(request, 'auth_view.html', context)


