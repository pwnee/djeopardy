from django.db import models
from django.contrib.auth.models import User

class FinalJeopardy(models.Model):
    category = models.CharField(max_length=200)    
    clue_text = models.CharField(max_length=2000)
    correct_answer = models.CharField(max_length=2000)
    game_number = models.CharField(max_length=200)
    game_id = models.CharField(max_length=200)
    air_date = models.DateField()
    scrape_date = models.DateField()
    game_round = models.CharField(max_length=20)
    category_comments = models.CharField(max_length=2000)
    game_url = models.CharField(max_length=500)

    def __unicode__ (self):
        return self.category

class Contestant(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    total_cash = models.IntegerField()      
    wager = models.IntegerField()     
    
    def __unicode__ (self):
        return self.user

class UserAnswer(models.Model):
    user = models.ForeignKey(User)
    question = models.IntegerField()
    answered = models.IntegerField()
    correct = models.IntegerField()


def createUserProfile(sender, user, request, **kwargs):    
    Contestant.objects.get_or_create(user=user)
    user_registered.connect(createUserProfile)