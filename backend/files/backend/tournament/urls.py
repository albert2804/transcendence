from django.urls import path
from .logic import startTournament
from .logic import signUpTwoDummies

urlpatterns = [
    path('logic/', startTournament),
    path('sign_up/', signUpTwoDummies)
]