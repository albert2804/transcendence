from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getData(request):
    person = {'message':"hello world", 'city': "Heilbronn", 'school': 42}
    return Response(person)