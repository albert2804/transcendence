from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
    state = request.GET.get('state')
    client_id = os.environ.get('42INTRA_CLIENT_ID')
    client_secret = os.environ.get('42INTRA_CLIENT_SECRET')
    url = "https://api.intra.42.fr/oauth/token"
    url += "?grant_type=authorization_code"
    url += "&client_id=" + client_id
    url += "&client_secret=" + client_secret
    url += "&code=" + code
    url += "&state=" + state
    url += "&redirect_uri=" + quote("https://" + request.get_host() + "/endpoint/auth/callback", safe='')

    response = requests.post(url)



    #TODO: handle error if there is no access_token
    token = response.json()['access_token'] 

    headers = {'Authorization': f'Bearer {token}'}
    endpoint = "https://api.intra.42.fr/v2/"
    response = requests.get(endpoint + "me/", headers=headers)

    user_details = ""
    if response.status_code == 200:
        user_details = response.json()
    else:
        print(f'Error authorizing with 42 intra: {response.status_code}')

    user, created = CustomUser.objects.get_or_create(
        username=user_details['login'],
        defaults={'email': user_details['email'],
                  'is_42_login': True })

    if user is not None:
        backend = ModelBackend()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

    user.first_name = user_details['first_name']
    user.last_name = user_details['last_name']
    user.alias = user.username
    user.save()

    if created:
        image_get = requests.get(user_details['image']['versions']['small'])
        if image_get.status_code == 200:
            print("IMAGE GET OK")
            image_content = ContentFile(image_get.content)
            # image_path = ("profilepic/" + user.username + "_avatar.jpg")
            # image_path = os.path.join(settings.MEDIA_ROOT, image_path)
            # print("IMAGE PATH: " + image_path)
            user.profile_pic.save(f'{user.username}_42avatar.jpeg', image_content)
            user.save()
    print(user.profile_pic.url)
    frontend_route="/"
    return HttpResponseRedirect(f'http://{request.get_host()}/redirect?to={frontend_route}')


def home(request):
    context = {
        'tabs':tabs
    }
    return render(request, 'auth_view.html', context)


