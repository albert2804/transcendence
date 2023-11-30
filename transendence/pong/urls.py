from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('game/', views.game, name="game"),
	path('info/', views.info, name="info"),
]