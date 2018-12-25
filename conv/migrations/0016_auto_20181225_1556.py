# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0015_auto_20180303_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ronde',
            field=models.IntegerField(verbose_name='Ronde', choices=[(1, '1 : Samedi 14h−20h'), (2, '2 : Samedi à partir de 20h'), (3, '3 : Dimanche 10h-16h'), (4, '4 : Inter-ronde')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='editions',
            field=models.ManyToManyField(db_constraint='Editions this user attendented', to='conv.Edition', blank=True),
        ),
    ]
