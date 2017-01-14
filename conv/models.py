from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .user import User

def initCurrentConv():
    editions = Edition.objects.all()
    year = 0
    for edition in editions:
        if edition.year>year:
            year = edition.year
    return year

_currentConv=None

def currentConv():
    if currentConv!=None:
        _currentConv=initCurrentConv()
    return _currentConv

def currentConvObject():
    return Edition.objects.get(year=currentConv())

class Scenario(models.Model):
    name = models.CharField("Titre", max_length=200)
    min_players = models.IntegerField("Nombre minimal de PJ")
    max_players = models.IntegerField("Nombre maximal de PJ")
    description = models.TextField("Description", max_length=10000)
    system = models.CharField("Système", max_length=200, default="D&D, Appel de Cthulu ou autre...")
    author = models.ForeignKey("conv.User", related_name="submitted_scenario_set")
    conv = models.ForeignKey("conv.Edition",related_name="conv")
    players = models.ManyToManyField("conv.User", blank=True)
    ronde = models.IntegerField("Ronde", choices=((1, "1 : Samedi 14h−20h"), (2, "2 : Samedi à partir de 20h"), (3, "3 : Dimanche 10h-16h")))
    validated = models.BooleanField("Validé", default=False)

    @property
    def complet(self):
        return self.players.count()>=self.max_players

    def allowedaccess(self, user=None):
        return True

    #def allowedaccess(self, user):
    #    print(blop)
    #    return user.isStaff or (author == user)

    def clean(self):
        if not (0<self.min_players<=self.max_players<=settings.MAX_N_PLAYERS):
            raise ValidationError({
                "min_players":"On doit avoir 0<min_players<=max_players<={}".format(settings.MAX_N_PLAYERS),
                "max_players":"On doit avoir 0<min_players<=max_players<={}".format(settings.MAX_N_PLAYERS)
                })
        if self.validated and not self.ronde:
            raise ValidationError({"ronde":"Il faut affecter une ronde au scénario avant de le valider"})

    def playermails(self):
        s=""
        for player in self.players.all():
            s+=player.email+";"
        if len(s)>0:
            s=s[0:-1]
        return s

    def __str__(self):
        return self.name + ("" if self.validated else "[unvalidated]")

class Event(models.Model):
    name = models.CharField("Titre", max_length=200)
    min_players = models.IntegerField("Nombre minimal de PJ", default=4)
    max_players = models.IntegerField("Nombre maximal de PJ", default=20)
    description = models.TextField("Description", max_length=10000)
    conv = models.ForeignKey("conv.Edition",related_name="even_conv")
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

class Edition(models.Model):
    year = models.PositiveIntegerField(_('Année de la Conv'),primary_key=True)
    start = models.DateField(_('Jour de début de la Conv'))
    end = models.DateField(_('Jour de fin de la Conv'))

    def __str__(self):
        return str(self.year)


class Sponsor(models.Model):
    name = models.CharField("Nom affiché", max_length=200)
    url = models.URLField("Site Web", max_length=200)
    logo = models.ImageField("Image à afficher")
    active = models.BooleanField("Affichable", default=True)
    conv = models.ForeignKey("conv.Edition",related_name="sponsor_conv")
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
