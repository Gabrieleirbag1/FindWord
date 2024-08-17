from django.db import models
from django.contrib.auth.models import User

class GameModel(models.Model):
    player1 = models.CharField(max_length=100, blank=True, null=True, default=None)
    player2 = models.CharField(max_length=100, blank=True, null=True, default=None)
    in_game_state = models.BooleanField(default=False)
    player1_ready = models.BooleanField(default=False)
    player2_ready = models.BooleanField(default=False)
    player1_text = models.CharField(max_length=100, blank=True, null=True, default="")
    player2_text = models.CharField(max_length=100, blank=True, null=True, default="")
    word = models.CharField(max_length=100)
    note = models.IntegerField(null=True, blank=True)
    score = models.FloatField(default=0)
    player1_note = models.IntegerField(blank=True, null=True, default=None)
    player2_note = models.IntegerField(blank=True, null=True, default=None)
    room_name = models.CharField(max_length=100)

    def __str__(self):
        return 

    def __unicode__(self):
        return
    
class FriendsModel(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_user2')
    score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username} : {self.score}"

    def __unicode__(self):
        return self.__str__()
    
class BugModel (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    bug = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bug}"

    def __unicode__(self):
        return self.__str__()
