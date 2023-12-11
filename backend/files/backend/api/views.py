from django.http import JsonResponse

def getTestData(request):
    test = {'message':"hello world", 'city': "Heilbronn", 'school': 42}
    return JsonResponse(test)