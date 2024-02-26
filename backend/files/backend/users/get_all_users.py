from django.http import JsonResponse
from api.models import CustomUser
from django.views import View

class GetAllUsersView(View):
    def get(self, request, *args, **kwargs):
        attributes = request.GET.get('attributes', '').split(',')
        print(f"Attributes: {attributes}")
        users = CustomUser.objects.all()
        users_list = [{ attr: getattr(user, attr, None) for attr in attributes } for user in users ]
        users_list_sorted = sorted(users_list, key=lambda x: x['mmr'], reverse=True)
        print (f"\nUsers List: {users_list}")
        return(JsonResponse({ 'response': users_list }))
