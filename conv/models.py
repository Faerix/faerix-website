from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

from .user import User

class Scenario(models.Model):
    name = models.CharField("Titre", max_length=200)
    min_players = models.IntegerField("Nombre minimal de PJ")
    max_players = models.IntegerField("Nombre maximal de PJ")
    description = models.TextField("Description", max_length=10000)
    system = models.CharField("Système", max_length=200, default="D&D, Appel de Cthulu ou autre...")
    author = models.ForeignKey("conv.User", related_name="submitted_scenario_set")
    players = models.ManyToManyField("conv.User", blank=True)
    ronde = models.IntegerField("Ronde", choices=((1, "1 : Samedi 14h−20h"), (2, "2 : Samedi à partir de 20h"), (3, "3 : Dimanche 10h-16h")))
    validated = models.BooleanField("Validé", default=False)

    @property
    def complet(self):
        return self.players.count()>=self.max_players

    def clean(self):
        if not (0<self.min_players<=self.max_players<=settings.MAX_N_PLAYERS):
            raise ValidationError({
                "min_players":"On doit avoir 0<min_players<=max_players<={}".format(settings.MAX_N_PLAYERS),
                "max_players":"On doit avoir 0<min_players<=max_players<={}".format(settings.MAX_N_PLAYERS)
                })
        if self.validated and not self.ronde:
            raise ValidationError({"ronde":"Il faut affecter une ronde au scénario avant de le valider"})

    def __str__(self):
        return self.name + ("" if self.validated else "[unvalidated]")

class Event(models.Model):
    name = models.CharField("Titre", max_length=200)
    min_players = models.IntegerField("Nombre minimal de PJ", default=4)
    max_players = models.IntegerField("Nombre maximal de PJ", default=20)
    description = models.TextField("Description", max_length=10000)
    players = models.ManyToManyField("conv.User", blank=True)
    ronde = models.IntegerField("Ronde", choices=((1, "1 : Samedi 14h−20h"), (2, "2 : Samedi à partir de 20h"), (3, "3 : Dimanche 10h-16h")))
    
    @property
    def complet(self):
        return self.players.count()>=self.max_players

    def clean(self):
        if not (0<self.min_players<=self.max_players<=settings.MAX_N_PLAYERS):
            raise ValidationError({
                "min_players":"On doit avoir 0<min_players<=max_players<={}".format(settings.MAX_N_PLAYERS),
                "max_players":"On doit avoir 0<min_players<=max_players<={}".format(settings.MAX_N_PLAYERS)
                })


    def __str__(self):
        return self.name

class Sponsor(models.Model):
    name = models.CharField("Nom affiché", max_length=200)
    url = models.URLField("Site Web", max_length=200)
    logo = models.ImageField("Image à afficher")
    active = models.BooleanField("Affichable", default=True)
    def __str__(self):
        return self.name

class News(models.Model):
    class Meta:
        verbose_name="News Item"
        verbose_name_plural="News"
    name = models.CharField("Titre", max_length=200)
    description = models.TextField("Texte", max_length=10000)
    visible_from = models.DateTimeField("Visible à partir de", default=timezone.now)
    visible_up_to = models.DateTimeField("Visible jusqu'à", default=timezone.now)

    def clean(self):
        if not self.visible_from < self.visible_up_to:
            raise ValidationError("La date de début doit précéder la date de fin :)")

    def __str__(self):
        return self.name
