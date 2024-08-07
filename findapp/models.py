from django.db import models
from django.contrib.auth.models import User

class GameModel(models.Model):
    player1 = models.CharField(max_length=100, blank=True, null=True)
    player2 = models.CharField(max_length=100, blank=True, null=True)
    in_game_state = models.BooleanField(default=False)
    player1_text = models.CharField(max_length=100, blank=True, null=True, default="")
    player2_text = models.CharField(max_length=100, blank=True, null=True, default="")
    word = models.CharField(max_length=100)
    note = models.IntegerField(null=True, blank=True)
    player1_note = models.IntegerField(null=True, blank=True, default=3)
    player2_note = models.IntegerField(null=True, blank=True, default=3)
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return 

    def __unicode__(self):
        return
