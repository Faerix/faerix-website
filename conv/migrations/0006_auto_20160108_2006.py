# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0005_auto_20160101_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='0000000000', verbose_name='Numéro de téléphone', help_text='Numéro de téléphone au format « 0612345678 »', validators=[django.core.validators.RegexValidator('\\d\\d ?\\d\\d ?\\d\\d ?\\d\\d ?\\d\\d', 'Entrez un numéro de téléphone valide de la forme 0612345678')], max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(verbose_name='email address', unique=True, max_length=254, error_messages={'unique': 'Un autre utilisateur a déjà cette adresse de courriel.'}),
        ),
    ]
