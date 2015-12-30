# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=254, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], unique=True, verbose_name="Nom d'utilisateur/pseudo", error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 254 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        ),
    ]
