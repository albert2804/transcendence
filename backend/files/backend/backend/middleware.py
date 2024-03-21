from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import jwt
from django.conf import settings

class ExpiredSignatureError(Exception):
    pass

class DecodeError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class InvalidTokenError(Exception):
    pass

class JWTCookieAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_token = request.COOKIES.get('jwt_token')
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')
                user = get_user_model().objects.get(id=user_id)
                request.user = user
            except jwt.ExpiredSignatureError:
                request.User = AnonymousUser()
                request.delete_jwt_cookie = True
            except jwt.DecodeError:
                request.User = AnonymousUser()
                raise DecodeError('Error decoding JWT token')
            except get_user_model().DoesNotExist:
                request.delete_jwt_cookie = True
                request.User = AnonymousUser()
            except jwt.InvalidTokenError:
                request.delete_jwt_cookie = True
                request.User = AnonymousUser()
        else:
            request.User = AnonymousUser()
        response = self.get_response(request)
        return response

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header and authorization_header.startswith('Bearer '):
            jwt_token_parts = authorization_header.split(' ')
            if len(jwt_token_parts) > 1:  # check if JWT token is present
                jwt_token = jwt_token_parts[1]  # get JWT token after 'Bearer'
                try:
                    payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
                    user_id = payload.get('user_id')
                    user = get_user_model().objects.get(id=user_id)
                    request.user = user
                except jwt.ExpiredSignatureError:
                    return JsonResponse({'error': 'JWT token has expired'}, status=401)
                except jwt.DecodeError:
                    return JsonResponse({'error': 'Error decoding JWT token'}, status=400)
                except get_user_model().DoesNotExist:
                    return JsonResponse({'error': 'User not found'}, status=404)
                except jwt.InvalidTokenError:
                    return JsonResponse({'error': 'Invalid JWT token'}, status=400)
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        return csrf_exempt(view_func)(request, *view_args, **view_kwargs)


class DeleteJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if getattr(request, 'jwt_token', False):
            response.delete_cookie('jwt_cookie_name')
        return response

# class SessionIdHeaderMiddleware:
# 	def __init__(self, get_response):
# 		self.get_response = get_response

# 	def __call__(self, request):
# 		#  get session id from header (sent as "Bearer <session_id>" as 'Authorization' header)
# 		# (django converts headers to uppercase and adds HTTP_ prefix)
# 		authorization_header = request.META.get('HTTP_AUTHORIZATION')
# 		if authorization_header:
# 			session_key = authorization_header.split(' ')[1] # get session id after 'Bearer'
# 			try:
# 				session = Session.objects.get(session_key=session_key)
# 				user_id = session.get_decoded().get('_auth_user_id')
# 				user = get_user_model().objects.get(id=user_id)
# 				request.user = user
# 			except:
# 				pass
# 		response = self.get_response(request)
# 		return response
	
# 	def process_view(self, request, view_func, view_args, view_kwargs):
# 		return csrf_exempt(view_func)(request, *view_args, **view_kwargs)