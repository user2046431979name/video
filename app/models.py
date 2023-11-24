from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Count

# Create your models here.
class Admin(models.Model):
    selectedUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Team(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False)
    cover = models.ImageField()
    description = models.TextField()
    counter = models.IntegerField(default=0)
    def count_videos(self):
        return self.videos_set.count()

class Videos(models.Model):
    teamobject = models.ForeignKey(Team, on_delete=models.CASCADE)
    videos = models.FileField()
    title = models.CharField(max_length=100)
    number = models.IntegerField()
class Message(models.Model):
    message = models.TextField()
    user = models.CharField(max_length=250)


class Comments(models.Model):
    text = models.TextField()
    teamobject = models.ForeignKey(Team,on_delete=models.CASCADE)
    user = models.CharField(max_length=250)
