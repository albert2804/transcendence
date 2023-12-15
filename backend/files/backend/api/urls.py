from django.urls import path
from . import views

urlpatterns = [
    path('csrf', views.get_csrf),
    path('test_json', views.getTestJsonData),
    path('test_text', views.getTestTextData),
    path('auth_status', views.get_auth_status),
    path('userlogin', views.userlogin),
    path('userlogout', views.userlogout),
]