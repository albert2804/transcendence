from django.http import JsonResponse
from api.models import CustomUser
from django.views import View

class GetAllUsersView(View):
    def get(self, request, *args, **kwargs):
        attributes = request.GET.get('attributes', '').split(',')
        print(f"Attributes: {attributes}")
        users = CustomUser.objects.all()
        users_list = [{ attr: getattr(user, attr, None) for attr in attributes } for user in users ]
        
        print (f"Users List: {users_list}")  # Print to console
        return(JsonResponse({ 'response': users_list }))
