from django.http import JsonResponse, HttpResponse
from .models import Statistics
from api.models import CustomUser

RED = "\033[31m"
RESET = "\033[0m"
# sends the statistics of the user as response to the frontend 
def send_userinfo(request):
	if request.user.is_authenticated:
		try:
			username = request.GET.get('username', '')
			if not username or username == 'undefined':
				username = request.user
			user_data = CustomUser.objects.get(username=username)
		except Exception as e: 
			return JsonResponse({'error': f'Could not get statistics data for user. Error: {str(e)}'}, status=500)
		try:
			response_data = {
				'username': user_data.username,
				#'date_joined':statistics_data.user.date_joined,
				'alias': user_data.alias,
				'games_played': user_data.num_games_played,
				'games_won': user_data.num_games_won,
				#'mmr':statistics_data.mmr,
				#'ranking':statistics_data.ranking,
				}
			return JsonResponse(response_data,
				status=200)
		except:
			return JsonResponse({'error': 'No statistics data found for the user'},
					status=404)
	else:
		return JsonResponse({'error': 'User not authenticated'},
			status=401)

# sends the profilepic url as a response to the frontend if GET method is active
#  if POST method is active, change the profilepici nside the database and save the file to MEDIA Root/profilepic
def handle_profilepic(request):
	if request.user.is_authenticated:
		if request.method == 'GET':
			try:
				username = request.GET.get('username', '')
				if not username or username == 'undefined':
					username = request.user
				profilepic_url = CustomUser.objects.get(username=username).profile_pic.url
				print(f"{profilepic_url}")
				return JsonResponse({'url': profilepic_url},
					status=200)
			except:
				return JsonResponse({'error': 'No Profile Picture found for the user'},
						status=404)
		elif request.method == 'POST':
			try:
				user = CustomUser.objects.get(username=request.user)
				if 'newPic' in request.FILES:
					user.profile_pic = request.FILES['newPic']
					user.save()
					print(f"{RED}user.profile_pic.url: {user.profile_pic.url}{RESET}")
					print(f"{RED}user.profile_pic: {user.profile_pic}{RESET}")
					return JsonResponse({'url': user.profile_pic.url}, status=200)
				else:
					return JsonResponse({'error': 'No Profile Picture found for the user'}, status=404)
			except CustomUser.DoesNotExist:
				return JsonResponse({'error': 'User not found'}, status=404)
			except Exception as e:
				return JsonResponse({'error': 'Changing profilePic failed'}, status=400) 
	else:
		return JsonResponse({'error': 'User not authenticated'},
			status=401)

# sends the results of the games which the user played as response to the frontend
# def send_usergames(request):
	
# 	return JsonResponse({})
