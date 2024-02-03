from django.http import JsonResponse, HttpResponse
from .models import Statistics
from api.models import CustomUser


# sends the statistics of the user as response to the frontend 
def send_userinfo(request):
	if request.user.is_authenticated:
		try:
			statistics_data, created = Statistics.objects.get_or_create(user=request.user)
		except Exception as e: 
			return JsonResponse({'error': f'Could not get statistics data for user. Error: {str(e)}'}, status=500)
		try:
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

def send_profilepic(request):
	if request.user.is_authenticated:
		try:
			profilepic_url = CustomUser.objects.get(username=request.user).profile_pic.url
			print(f"{profilepic_url}")
			return JsonResponse({'url': profilepic_url},
				status=200)
		except:
			return JsonResponse({'error': 'No Profile Picture found for the user'},
					status=404)
	else:
		return JsonResponse({'error': 'User not authenticated'},
			status=401)

def uploadpicture(request):
    try:
        if request.method == 'POST':
            user = CustomUser.objects.get(username=request.user)
            if 'newPic' in request.FILES:
                user.profile_pic = request.FILES['newPic']
                user.save()
                print(f"user.profile_pic.url: {user.profile_pic.url}")
                print(f"user.profile_pic: {user.profile_pic}")
                return JsonResponse({'url': user.profile_pic.url}, status=200)
            else:
                return JsonResponse({'error': 'No Profile Picture found for the user'}, status=404)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': 'Changing profilePic failed'}, status=400)




# sends the results of the games which the user played as response to the frontend
# def send_usergames(request):
	
# 	return JsonResponse({})
