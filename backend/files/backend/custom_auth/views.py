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

# def index(request):
#     return HttpResponse("Hello, world. You're at the auth index.")

tabs = [
    {'name':'home', 'dir':"/endpoint/auth/"},
    {'name':'callback', 'dir':"/endpoint/auth/callback/"},
]

def success(request):
    return HttpResponse("This is the success view.")

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

# @psa("social:complete")
# def ajax_auth(request, backend):
#     """AJAX authentication endpoint"""
#     if isinstance(request.backend, BaseOAuth1):
#         token = {
#             "oauth_token": request.REQUEST.get("access_token"),
#             "oauth_token_secret": request.REQUEST.get("access_token_secret"),
#         }
#     elif isinstance(request.backend, BaseOAuth2):
#         token = request.REQUEST.get("access_token")
#     else:
#         raise HttpResponseBadRequest("Wrong backend type")
#     user = request.backend.do_auth(token, ajax=True)
#     login(request, user)
#     data = {"id": user.id, "username": user.username}
#     return HttpResponse(json.dumps(data), mimetype="application/json")


# @psa('social:complete')
# def register_by_access_token(request):
#     # This view expects an access_token GET parameter, if it's needed,
#     # request.backend and request.strategy will be loaded with the current
#     # backend and strategy.
#     logger.warning("REGISTER BY ACCESS TOKEN")
#     token = request.REQUEST.get('access_token')
#     print("TOKEN: " + token)
#     user = request.backend.do_auth(token)
#     logger.warning("USER: " + user)
#     login(request, user)
#     print ("USER: " + user)
#     data = {"id": user.id, "username": user.username, "provider" : ""}
#     return HttpResponse(json.dumps(data), mimetype="application/json")
#     #return render(request, 'auth_view.html', context)
    
# def home(request):
#     context = {
#         'tabs':tabs
#     }
#     print("HHHHORCEODRECCHSCUCHRSEHOSU")
#     return render(request, 'auth_view.html', context)

# def social_login(request):
#     return render(request,'auth_view.html')

