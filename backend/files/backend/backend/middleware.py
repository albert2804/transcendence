from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

class SessionIdHeaderMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		#  get session id from header (sent as "Bearer <session_id>" as 'Authorization' header)
		# (django converts headers to uppercase and adds HTTP_ prefix)
		authorization_header = request.META.get('HTTP_AUTHORIZATION')
		if authorization_header:
			session_key = authorization_header.split(' ')[1] # get session id after 'Bearer'
			try:
				session = Session.objects.get(session_key=session_key)
				user_id = session.get_decoded().get('_auth_user_id')
				user = get_user_model().objects.get(id=user_id)
				request.user = user
			except:
				pass
		response = self.get_response(request)
		return response
	
	def process_view(self, request, view_func, view_args, view_kwargs):
		return csrf_exempt(view_func)(request, *view_args, **view_kwargs)