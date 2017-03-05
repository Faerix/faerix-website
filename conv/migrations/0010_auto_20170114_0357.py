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
                ('year', models.PositiveIntegerField(serialize=False, verbose_name='Année de la Conv', primary_key=True)),
                ('start', models.DateField(verbose_name='Jour de début de la Conv')),
                ('end', models.DateField(verbose_name='Jour de fin de la Conv')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='conv',
            field=models.ForeignKey(to='conv.Edition', default=2017, related_name='even_conv'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scenario',
            name='conv',
            field=models.ForeignKey(to='conv.Edition', default=2017, related_name='conv'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='editions',
            field=models.ManyToManyField(db_constraint='Editions this user attendented', to='conv.Edition'),
        ),
    ]
