# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0007_auto_20160111_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario',
            name='universe',
        ),
        migrations.AddField(
            model_name='scenario',
            name='system',
            field=models.CharField(max_length=200, verbose_name='Système', default='D&D, Appel de Cthulu ou autre...'),
        ),
    ]
