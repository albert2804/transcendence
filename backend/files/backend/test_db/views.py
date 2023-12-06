from django.shortcuts import render
from .models import Players

tabs = [
	{'name':'home', 'dir':"/endpoint/test_db/"},
	{'name':'game', 'dir':"/endpoint/test_db/game"},
	{'name':'info', 'dir':"/endpoint/test_db/info"},
]

def home(request):
	context = {
		'tabs':tabs
	}
	return render(request, 'home.html', context)

def game(request):
	context = {
		'tabs':tabs
	}
	return render(request, 'game.html', context)

def info(request):
	players = Players.objects.all()
	context = {
		'tabs':tabs,
		'players':players
	}	
	return render(request, 'info.html', context)
