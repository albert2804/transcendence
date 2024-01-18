from django.db import models
from django.conf import settings
import logging
logger = logging.getLogger(__name__)

#from social_django.models import UserSocialAuth
from social_core.backends.oauth import BaseOAuth2
from urllib.parse import urlencode

SOCIAL_AUTH_PIPELINE = (
    'custom_auth.models.foo'
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
#    'custom_auth.pipeline',  # <--- set the path to the function
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


class Intra42OAuth2(BaseOAuth2):
    """GitHub OAuth authentication backend"""
    name = '42_intra_oauth'
                        #'https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-3c7e6b5f041d92a81665a41cf1fe7244fce02d09e64f7d39e5c5ee13da9018da&response_type=code?client_id=None&redirect_uri=http%3A%2F%2Flocalhost%2Fendpoint%2Fauth%2Fcomplete%2F42_intra_oauth%2F%3Fredirect_state%3DMZGSGWtCvB0SdIKDoYiOzStEc5vizkJh&state=MZGSGWtCvB0SdIKDoYiOzStEc5vizkJh&response_type=code&grant_type=client_credentials'
    #AUTHORIZATION_URL = 'https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-3c7e6b5f041d92a81665a41cf1fe7244fce02d09e64f7d39e5c5ee13da9018da&response_type=code'
    
    #https://api.intra.42.fr/oauth/authorize?client_id=None&redirect_uri=http%3A%2F%2Flocalhost%2Fendpoint%2Fauth%2Fcomplete%2F42_intra_oauth%2F%3Fredirect_state%3DMZGSGWtCvB0SdIKDoYiOzStEc5vizkJh&state=MZGSGWtCvB0SdIKDoYiOzStEc5vizkJh&response_type=code&grant_type=client_credentials
    AUTHORIZATION_URL='https://api.intra.42.fr/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://api.intra.42.fr/oauth/token/'
    ACCESS_TOKEN_METHOD = 'POST'
    LOGIN_REDIRECT_URL='https://localhost/endpoint/auth/'
    KEY='u-s4t2ud-3c7e6b5f041d92a81665a41cf1fe7244fce02d09e64f7d39e5c5ee13da9018da'
    # old secret
    #SECRET='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'


    UID = 'u-s4t2ud-3c7e6b5f041d92a81665a41cf1fe7244fce02d09e64f7d39e5c5ee13da9018da'
    # next secret, valid after 29/12/2023
    SECRET='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'

    # SCOPE_SEPARATOR = ','
    # ID_KEY = 'id'
    # EXTRA_DATA = [
    #     ('grant_type', 'authorization_code'),
    #     ('client_id', UID),
    #     ('client_secret', SECRET),
    #     ('code', )
    # ]

    def auth_params(self, *args, **kwargs):
        print ("AUTH_PARAMS!!!")
        params = super().auth_params(*args, **kwargs)
        params = {"client_id": self.KEY, "redirect_uri": self.LOGIN_REDIRECT_URL}
        #params["client_secret"] = self.SECRET
        #params["grant_type"] = "authorization_code"
        #params["code"] = "123456789"
        params['response_type'] = 'code'
        return params

    def get_user_details(self, response):
        """Return user details from 42 intra account"""
        print("RESPONSE:\n\n\n" + response + "\n\n\n")
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        print("USER_DATA!!!")
        url = 'https://api.intra.42.fr/v2/users' + urlencode({
            'access_token': access_token
        })
        return self.get_json(url)

def foo(strategy, details, response, is_new=False, user=None, *args, **kwargs):
    print ("FOOOOOOOOOOOOOOOO")
    logger.error("foooooooo")