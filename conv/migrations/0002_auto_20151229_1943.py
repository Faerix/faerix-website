# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name_plural': 'News', 'verbose_name': 'News Item'},
        ),
        migrations.AddField(
            model_name='scenario',
            name='min_players',
            field=models.IntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='event',
            name='ronde',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)]),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='max_players',
            field=models.IntegerField(default=6),
        ),
    ]
