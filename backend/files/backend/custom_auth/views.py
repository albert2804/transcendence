from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
import os
from urllib.parse import quote
from api.models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import logging
logger = logging.getLogger(__name__)

tabs = [
    {'name':'home', 'dir':"/endpoint/auth/"},
    {'name':'callback', 'dir':"/endpoint/auth/callback/"},
]


def callback(request):
    code = request.GET.get('code')
    print("HOST: " + request.get_host())
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
    url += "&redirect_uri=" + quote("https://" + request.get_host() + "/endpoint/auth/callback", safe='')

    print("URL: " + url)
    response = requests.post(url)
    print(response.json())
    print (response.text)


    #TODO: handle error if there is no access_token
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

    print ("IMAGE LINK: ")
    print(user_details['image']['versions']['small'])
    print(user_details['first_name'])
    print(user_details['last_name'])
    user.first_name = user_details['first_name']
    user.last_name = user_details['last_name']
    user.alias = user.username
    user.save()


    image_get = requests.get(user_details['image']['versions']['small'])

    if image_get.status_code == 200:
        print("IMAGE GET OK")
        image_content = ContentFile(image_get.content)
        if not default_storage.exists(user.username + "_avatar.jpg"):
            user.profile_pic.save(f'{user.username}_avatar.jpg', image_content)
            user.save()
    print(user.profile_pic.url)
    # print(f"username: {user_details['login']}")

    return HttpResponse("This is the callback view.\n") # + json.dumps(user_details)


def home(request):
    context = {
        'tabs':tabs
    }

    return render(request, 'auth_view.html', context)


