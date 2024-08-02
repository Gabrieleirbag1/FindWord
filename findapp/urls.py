# urls.py
from django.urls import path
from .views import Game, Lobby  

urlpatterns = [
    path('game/<int:id>/', Game.as_view(), name='game'),
    path('lobby/', Lobby.as_view(), name='lobby'),
    path('', Lobby.as_view(), name='lobby'),
]