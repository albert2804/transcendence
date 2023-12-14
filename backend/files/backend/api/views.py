from django.http import JsonResponse, HttpResponse

# application/json
def getTestJsonData(request):
    test = {'message':"hello world", 'city': "Heilbronn", 'school': 42}
    return JsonResponse(test)

# text/plain or text/html
def getTestTextData(request):
    return HttpResponse("Hello World")

# get auth status of user
def get_auth_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True})
    else:
        return JsonResponse({'authenticated': False})

