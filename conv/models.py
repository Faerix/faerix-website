from django.db import models
from django.utils import timezone

from .user import User

class Scenario(models.Model):
    name = models.CharField(max_length=200)
    max_players = models.IntegerField(default=6)
    min_players = models.IntegerField(default=3)
    description = models.TextField(max_length=10000)
    universe = models.CharField(max_length=200)
    author = models.ForeignKey("conv.User", related_name="campaigns")
    players = models.ManyToManyField("conv.User")
    ronde = models.IntegerField(blank=True, choices=((1, 1), (2, 2), (3, 3)))
    validated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    max_players = models.IntegerField(default=4)
    description = models.TextField(max_length=10000)
    players = models.ManyToManyField("conv.User")
    ronde = models.IntegerField(choices=((1, 1), (2, 2), (3, 3)))
    def __str__(self):
        return self.name

class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    logo = models.ImageField()
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class News(models.Model):
    class Meta:
        verbose_name="News Item"
        verbose_name_plural="News"
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=10000)
    visible_from = models.DateTimeField(default=timezone.now)
    visible_up_to = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
