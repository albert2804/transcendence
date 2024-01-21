# from django.db import models
# from django.conf import settings
import logging
import json
import requests

logger = logging.getLogger(__name__)

#from social_django.models import UserSocialAuth
from social_core.backends.oauth import BaseOAuth2
from urllib.parse import urlencode

# SOCIAL_AUTH_PIPELINE = (
#     'custom_auth.models.foo',
#     'social_core.pipeline.social_auth.social_details',
#     'social_core.pipeline.social_auth.social_uid',
#     'social_core.pipeline.social_auth.auth_allowed',
#     'social_core.pipeline.social_auth.social_user',
#     'social_core.pipeline.user.get_username',
#     'social_core.pipeline.user.create_user',
# #    'custom_auth.pipeline',  # <--- set the path to the function
#     'social_core.pipeline.social_auth.associate_user',
#     'social_core.pipeline.social_auth.load_extra_data',
#     'social_core.pipeline.user.user_details',
# )


class Intra42OAuth2(BaseOAuth2):
    """GitHub OAuth authentication backend"""
    name = 'intra42_oauth2'
                        #'https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-3c7e6b5f041d92a81665a41cf1fe7244fce02d09e64f7d39e5c5ee13da9018da&response_type=code?client_id=None&redirect_uri=http%3A%2F%2Flocalhost%2Fendpoint%2Fauth%2Fcomplete%2F42_intra_oauth%2F%3Fredirect_state%3DMZGSGWtCvB0SdIKDoYiOzStEc5vizkJh&state=MZGSGWtCvB0SdIKDoYiOzStEc5vizkJh&response_type=code&grant_type=client_credentials'
    AUTHORIZATION_URL = 'https://api.intra.42.fr/oauth/authorize/'
    
    #https://api.intra.42.fr/oauth/authorize?client_id=None&redirect_uri=http%3A%2F%2Flocalhost%2Fendpoint%2Fauth%2Fcomplete%2F42_intra_oauth%2F%3Fredirect_state%3DMZGSGWtCvB0SdIKDoYiOzStEc5vizkJh&state=MZGSGWtCvB0SdIKDoYiOzStEc5vizkJh&response_type=code&grant_type=client_credentials
    ENDPOINT = "https://api.intra.42.fr/v2/"
    ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token/'
    ACCESS_TOKEN_METHOD = 'POST'
    LOGIN_REDIRECT_URL='https://localhost/endpoint/auth/complete/intra42_oauth2'
    STATE_PARAMETER = True
    KEY='u-s4t2ud-3c7e6b5f041d92a81665a41cf1fe7244fce02d09e64f7d39e5c5ee13da9018da'

    UID = 'u-s4t2ud-3c7e6b5f041d92a81665a41cf1fe7244fce02d09e64f7d39e5c5ee13da9018da'
    SECRET='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'
    CLIENT = UID
    SOCIAL_AUTH_INTRA42_OAUTH2_KEY = 'u-s4t2ud-3c7e6b5f041d92a81665a41cf1fe7244fce02d09e64f7d39e5c5ee13da9018da'
    SOCIAL_AUTH_INTRA42_OAUTH2_SECRET = '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'
    # next secret, valid after 29/12/2023


    # SCOPE_SEPARATOR = ','
    # ID_KEY = 'id'
    # SOCIAL_AUTH_Intra42OAUTH2_EXTRA_DATA = [
    #     ('grant_type', 'client_credentials'),
    #     ('client_id', UID),
    #     ('client_secret', SECRET),
    #     ('response_type', 'code'),
    #     ('state', 'MZGSGWtffooCvB011SdIKD47oYiOzStEc23x5vizkJh')
    # ]

    def auth_params(self, *args, **kwargs):
        print ("AUTH_PARAMS!!!")
        params = super().auth_params(*args, **kwargs)
        print ("Params:" + json.dumps(params))
        #params["client_id"] = self.UID
        #params["client_secret"] = self.SECRET
        #params["grant_type"] = "authorization_code"
        
        # state = self.state_token()
        # print(state)
        # self.strategy.session_set('social_auth_{backend_name}_state'.format(backend_name=self.name), state)
        # print(state)
        #params['response_type'] = 'code'
        #print ("Params:" + json.dumps(params))
        return params

    def get_user_details(self, response):
        """Return user details from 42 intra account"""
        print("RESPONSE:\n\n\n" + json.dumps(response) + "\n\n\n")
        token = response.get('access_token')
        print("TOKEN: " + token)
        self.token = token

        headers = {'Authorization': f'Bearer {self.token}'}
        print(self.ENDPOINT + "me/")
        response = requests.get(self.ENDPOINT + "me/", headers=headers)

        if response.status_code == 200:
            user_details = response.json()
            #print(user_details)
        else:
            print(f'Error: {response.status_code}')

        print(f"username: {user_details['login']}")
        return {'username': user_details["login"],
                'social_user': user_details["login"],
                'email': user_details["email"] or '',
                'first_name': user_details["first_name"],
                'provider': "intra42_oauth2"}

    # def user_data(self, access_token, *args, **kwargs):
    #     """Loads user data from service"""
    #     print("USER_DATA!!!")
    #     url = 'https://api.intra.42.fr/v2/users' + urlencode({
    #         'access_token': access_token
    #     })
    #     return self.get_json(url)

    def get_redirect_uri(self, state=None):
        print ("GET_REDIRECT_URI!!!")
        print(self.LOGIN_REDIRECT_URL)
        return self.LOGIN_REDIRECT_URL
    
    def authorization_url(self):
        print ("AUTHORIZATION_URL!!!")
        print(self.AUTHORIZATION_URL)
        return self.AUTHORIZATION_URL
    

    def social_user(backend, uid, user=None, *args, **kwargs):
        provider = backend.name
        print("SOCIAL USER: provider: " + provider + " uid: " + uid)
        social = backend.strategy.storage.user.get_social_auth(provider, uid)
        if social:
            if user and social.user != user:
                print("Error: User already associated to %s account. % provider")
                #raise AuthAlreadyAssociated(backend)
            elif not user:
                user = social.user
        return {
            "social": social,
            "user": user,
            "is_new": user is None,
            "new_association": social is None,
        }

def foo(strategy, details, response, is_new=False, user=None, *args, **kwargs):
    print ("FOOOOOOOOOOOOOOOO")
    logger.error("foooooooo")