from django.contrib import admin

from conv import models

admin.site.register(models.User)
admin.site.register(models.Scenario)
admin.site.register(models.Event)
admin.site.register(models.Sponsor)
admin.site.register(models.News)
