from django.contrib import admin

from conv import models
from conv import forms

class ScenarioAdmin(admin.ModelAdmin):
    form = forms.CheckingScenarioForm

class EventAdmin(admin.ModelAdmin):
    form = forms.CheckingEventForm

admin.site.register(models.User)
admin.site.register(models.Scenario, ScenarioAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Sponsor)
admin.site.register(models.News)
