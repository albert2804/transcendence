from django.http import JsonResponse, HttpResponse
from api.models import CustomUser
from api.forms import CustomUserCreationForm
from django.shortcuts import redirect
import os, json

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
					try:
						print(f"{RED}TRY: {user.profile_pic}{RESET}")
						if user.profile_pic != "profilepic/default.jpeg":
							os.remove(f"/media/{user.profile_pic}")
					except:
						print(f"{RED}EXCEPT: {user.profile_pic}{RESET}")
						pass			
					user.profile_pic = request.FILES['newPic']
					user.save()
					print(f"{RED}POST: user.profile_pic.url: {user.profile_pic.url}{RESET}")
					print(f"{RED}POST: user.profile_pic: {user.profile_pic}{RESET}")
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

# TO-DO Redirect to login page again, so the user has to login woth his new password to update teh session
def verify(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			try:
				user = CustomUser.objects.get(username=request.user)
			except Exception as e: 
				return JsonResponse({'error': f'Could not get CustomUser. Error: {str(e)}'}, status=500)
			except CustomUser.DoesNotExist:
				return JsonResponse({'error': 'User not found'}, status=404)
			try:
				data = json.loads(request.body.decode('utf-8'))
				if user.check_password(data.get('old_pw')):
					user.set_password(data.get('password1'))
					user.save()
					return HttpResponse("password changed")
					# return redirect('login')
				else:
					return JsonResponse({'message': 'New password does not match with the old password'},
							status=500)
			except:
				return JsonResponse({'error': 'pw could not be updated'},
						status=500)
	else:
		return JsonResponse({'error': 'User not authenticated'},
			status=401)






# sends the results of the games which the user played as response to the frontend
# def send_usergames(request):
	
# 	return JsonResponse({})
