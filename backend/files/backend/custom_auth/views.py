from django.shortcuts import render
from django.http import HttpResponse
from custom_auth.models import Intra42OAuth2
from django.contrib.auth import login
from social_django.utils import psa
import json
import requests
import os
from urllib.parse import quote

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

    return HttpResponse("This is the callback view.\n" + "CODE: " + code + "\nURL called: " + url)

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


@psa('social:complete')
def register_by_access_token(request):
    # This view expects an access_token GET parameter, if it's needed,
    # request.backend and request.strategy will be loaded with the current
    # backend and strategy.
    logger.warning("REGISTER BY ACCESS TOKEN")
    token = request.REQUEST.get('access_token')
    print("TOKEN: " + token)
    user = request.backend.do_auth(token)
    logger.warning("USER: " + user)
    login(request, user)
    print ("USER: " + user)
    data = {"id": user.id, "username": user.username, "provider" : ""}
    return HttpResponse(json.dumps(data), mimetype="application/json")
    #return render(request, 'auth_view.html', context)
    
def home(request):
    context = {
        'tabs':tabs
    }
    print("HHHHORCEODRECCHSCUCHRSEHOSU")
    return render(request, 'auth_view.html', context)

# def social_login(request):
#     return render(request,'auth_view.html')

