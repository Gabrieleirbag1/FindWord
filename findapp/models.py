from django.db import models

class GameModel(models.Model):
    player1 = models.CharField(max_length=100, blank=True, null=True)
    player2 = models.CharField(max_length=100, blank=True, null=True)
    word = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return 

    def __unicode__(self):
        return
    
