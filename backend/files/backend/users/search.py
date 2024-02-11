from django.http import JsonResponse
from api.models import CustomUser
from django.db.models import Q
from django.views import View

class SearchUsersView(View):
    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')

        if search_query:
            search_results = CustomUser.objects.filter(Q(username__icontains=search_query))
            results_list = [{'id': user.id, 'name': user.username} for user in search_results]
        else:
            results_list = []

        # print(f"Search Results: {results_list}")  # Print to console

        return JsonResponse(results_list, safe=False)
