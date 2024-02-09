from django.http import JsonResponse, HttpResponse
from api.models import CustomUser

def search_users(request):
  search_query = request.GET.get('search', '')
  # if search_query:
  #   search_results = User.objects.filter(Q(name__icontains=search_query))
  #   results_list = [{'id': user.id, 'name': user.name} for user in search_results]
  # else:
  #   user_list = []

  return JsonResponse({'user': 'peter', 'user': 'alber', 'user': 'kathrin'})
