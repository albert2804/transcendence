from django.urls import path
from .logic import initTournament
from .logic import signUpTwoDummies
from .logic import readyPlayer
from .logic import getTournaments

urlpatterns = [
    path('logic/', initTournament),
    path('sign_up/', signUpTwoDummies),
    path('readyPlayer/', readyPlayer),
    path('getTournaments/', getTournaments)

]