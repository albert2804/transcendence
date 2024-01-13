from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.send_userinfo),
    # path('games/', views.send_usergames),
]