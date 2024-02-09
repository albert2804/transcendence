from django.urls import path
from . import views, search

urlpatterns = [
    path('info/', views.send_userinfo),
    path('profilepic/', views.handle_profilepic),
    path('search_query/', search.search_users)
]