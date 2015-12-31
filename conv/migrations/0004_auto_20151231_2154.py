# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0003_auto_20151230_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='min_players',
            field=models.IntegerField(default=4, verbose_name='Nombre minimal de PJ'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_players',
            field=models.IntegerField(default=20, verbose_name='Nombre maximal de PJ'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='event',
            name='ronde',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], verbose_name='Ronde'),
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Texte'),
        ),
        migrations.AlterField(
            model_name='news',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='news',
            name='visible_from',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Visible à partir de'),
        ),
        migrations.AlterField(
            model_name='news',
            name='visible_up_to',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Visible jusqu'à"),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='submitted_scenario_set'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='description',
            field=models.TextField(max_length=10000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='max_players',
            field=models.IntegerField(verbose_name='Nombre maximal de PJ'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='min_players',
            field=models.IntegerField(verbose_name='Nombre minimal de PJ'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='ronde',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], null=True, verbose_name='Ronde', blank=True),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='universe',
            field=models.CharField(default='D&D, Appel de Cthulu ou autre...', max_length=200, verbose_name='Univers'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='validated',
            field=models.BooleanField(default=False, verbose_name='Validé'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Affichable'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='logo',
            field=models.ImageField(upload_to='', verbose_name='Image à afficher'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nom affiché'),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='url',
            field=models.URLField(verbose_name='Site Web'),
        ),
    ]
