from django.db import models

# Create your models here.

from social_core.backends.oauth import BaseOAuth2

class Intra42OAuth2(BaseOAuth2):
    """GitHub OAuth authentication backend"""
    name = 'github'
    AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from GitHub account"""
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'first_name': response.get('name')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        url = 'https://api.github.com/user?' + urlencode({
            'access_token': access_token
        })
        return self.get_json(url)