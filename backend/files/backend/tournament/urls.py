from django.urls import path
from .logic import startTournament

urlpatterns = [
    path('logic/', startTournament),
]