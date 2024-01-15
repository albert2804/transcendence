from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.send_userinfo),
    path('profilepic/', views.send_profilepic),
    # path('games/', views.send_usergames),
]