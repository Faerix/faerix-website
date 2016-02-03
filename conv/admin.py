from django.contrib import admin
from hijack.admin import HijackUserAdminMixin

from conv import models
from conv import forms

class UserAdmin(admin.ModelAdmin, HijackUserAdminMixin):
        list_display = (
                "username",
                "first_name",
                "last_name",
                "phone",
                "email",
                "date_joined",
                "last_visit",
                "is_staff",
                'hijack_field',  # Hijack button
            )

class ScenarioAdmin(admin.ModelAdmin):
    form = forms.CheckingScenarioForm

class EventAdmin(admin.ModelAdmin):
    form = forms.CheckingEventForm

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Scenario, ScenarioAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Sponsor)
admin.site.register(models.News)
