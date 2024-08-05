from django.db import models
from django.contrib.auth.models import User

class GameModel(models.Model):
    player1 = models.CharField(max_length=100, blank=True, null=True)
    player2 = models.CharField(max_length=100, blank=True, null=True)
    in_game_state = models.BooleanField(default=False)
    word = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return 

    def __unicode__(self):
        return
