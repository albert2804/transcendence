from django.urls import path
from . import views
from .search import SearchUsersView
from .get_all_users import GetAllUsersView

urlpatterns = [
    path('verify/', views.verify),
    path('info/', views.send_userinfo, name='send_userinfo'),
    path('profilepic/', views.handle_profilepic),
    path('search/', SearchUsersView.as_view(), name='search_users'),
	path('get_all_users/', GetAllUsersView.as_view(), name='get_all_users'),
]