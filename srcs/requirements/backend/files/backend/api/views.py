from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getTestData(request):
    test = {'message':"hello world", 'city': "Heilbronn", 'school': 42}
    return Response(test)