from django.urls import path
from .logic import initTournament
from .logic import signUpTwoDummies

urlpatterns = [
    path('logic/', initTournament),
    path('sign_up/', signUpTwoDummies)
]