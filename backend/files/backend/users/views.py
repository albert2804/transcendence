from django.http import JsonResponse, HttpResponse
from .models import Statistics


# sends the statistics of the user as response to the frontend 
def send_userinfo(request):
	if request.user.is_authenticated:
		try:
			statistics_data = Statistics.objects.get(user=request.user)
			response_data = {
				'userid:':statistics_data.user.id,
				'username':statistics_data.user.username,
				'date_joined':statistics_data.user.date_joined, 
				'games_played':statistics_data.games_played,
				'mmr':statistics_data.mmr,
				'ranking':statistics_data.ranking,
				}
			return JsonResponse(response_data,
				status=200)
		except:
			return JsonResponse({'error': 'No statistics data found for the user'},
					status=404)
	else:
		return JsonResponse({'error': 'User not authenticated'},
			status=401)

# sends the results of the games which the user played as response to the frontend
# def send_usergames(request):
	
# 	return JsonResponse({})
