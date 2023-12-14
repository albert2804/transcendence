from django.urls import path
from . import views

urlpatterns = [
    path('test_json', views.getTestJsonData),
    path('test_text', views.getTestTextData),
    path('auth_status', views.get_auth_status),
]