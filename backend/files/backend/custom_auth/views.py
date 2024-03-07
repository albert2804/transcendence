from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
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
    code = request.GET.get('code', "")
    state = request.GET.get('state', "")
    client_id = os.environ.get('42INTRA_CLIENT_ID', "")
    client_secret = os.environ.get('42INTRA_CLIENT_SECRET', "")
    url = "https://api.intra.42.fr/oauth/token"
    url += "?grant_type=authorization_code"
    url += "&client_id=" + client_id
    url += "&client_secret=" + client_secret
    url += "&code=" + code
    url += "&state=" + state
    url += "&redirect_uri=" + quote("https://" + request.get_host() + "/endpoint/auth/callback", safe='')

    response = requests.post(url)

    if 'access_token' not in response.json():
        return HttpResponseRedirect(f'http://{request.get_host()}/login?error={error}')
    token = response.json()['access_token'] 

    headers = {'Authorization': f'Bearer {token}'}
    endpoint = "https://api.intra.42.fr/v2/"
    response = requests.get(endpoint + "me/", headers=headers)

    user_details = ""
    if response.status_code == 200:
        user_details = response.json()
    else:
        error = "Error authenticating with 42 intra."
        return HttpResponseRedirect(f'http://{request.get_host()}/login?error={error}')

    user = CustomUser.objects.filter(username=user_details['login']).first()
    if user is not None and user.is_42_login == False:
        error = "This account is already registered locally, please log in with username and password."
        return HttpResponseRedirect(f'http://{request.get_host()}/login?error={error}')

    user, created = CustomUser.objects.get_or_create( username=user_details['login'],
                        defaults={'email': user_details['email'], 'is_42_login': True, 'alias': user_details['login'] })
    if user is not None:
        backend = ModelBackend()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

    user.first_name = user_details['first_name']
    user.last_name = user_details['last_name']
    user.save()

    if created:
        image_get = requests.get(user_details['image']['versions']['small'])
        if image_get.status_code == 200:
            image_content = ContentFile(image_get.content)
            user.profile_pic.save(f'{user.username}_42avatar.jpeg', image_content)
            user.save()
    message = "Successfully logged in to 42 intra."
    return HttpResponseRedirect(f'http://{request.get_host()}/login?message={message}')
