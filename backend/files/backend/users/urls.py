from django.urls import path
from . import views
from .search import SearchUsersView

urlpatterns = [
    path('info/', views.send_userinfo),
    path('profilepic/', views.handle_profilepic),
    path('search/', SearchUsersView.as_view(), name='search_users'),
]