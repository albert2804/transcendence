from django.urls import path
from .logic import initTournament
from .logic import signUpTwoDummies
from .logic import inviteOtherPlayer
from .logic import getTournaments
from .logic import getTourmaentsGames

urlpatterns = [
    path('logic/', initTournament),
    path('sign_up/', signUpTwoDummies),
    path('iviteOtherPlayer/', inviteOtherPlayer),
    path('getTournaments/', getTournaments),
    path('getTourmaentsGames/', getTourmaentsGames)

]