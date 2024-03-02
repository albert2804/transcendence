from django.urls import path
from . import views

urlpatterns = [
    path('csrf', views.get_csrf),
    path('auth_status', views.get_auth_status),
    path('userlogin', views.userlogin, name='login'),
    path('userlogout', views.userlogout),
    path('userregister', views.userregister),
    path('invite_to_game', views.invite_to_game),
	path('move_paddle', views.move_paddle),
	path('get_leaderboard', views.get_leaderboard),
	path('get_friends', views.get_friends),
    path('add_friend', views.add_friend),
	path('remove_friend', views.remove_friend),
]