from django.shortcuts import render
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the auth index.")

tabs = [
    {'name':'home', 'dir':"/endpoint/auth/"},
]

def home(request):
    context = {
        'tabs':tabs
    }
    return render(request, 'auth_view.html', context)

def social_login(request):
    return render(request,'auth_view.html')