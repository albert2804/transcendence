from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.send_userinfo),
    path('profilepic/', views.handle_profilepic),
]