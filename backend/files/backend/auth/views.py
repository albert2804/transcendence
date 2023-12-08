from django.shortcuts import render
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the auth index.")

def social_login(request):
    return render(request,'social_login.html')