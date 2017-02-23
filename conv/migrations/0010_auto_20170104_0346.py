# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0009_auto_20160131_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('year', models.PositiveIntegerField(primary_key=True, verbose_name='Année de la Conv', serialize=False)),
                ('start', models.DateField(verbose_name='Jour de début de la Conv')),
                ('end', models.DateField(verbose_name='Jour de fin de la Conv')),
            ],
        ),
    ]
