from django.http import JsonResponse
import json

def startTournament(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      data = json.loads(request.body)
      print("gotten message\n");
      #TODO: implement player name check
      #TODO: create games as objects
      #TODO: implement tournament logic
      #TODO: finished
      return JsonResponse({'message': 'Data received'})
    else:
      return JsonResponse({'error': 'Invalid request'}, status=400)
