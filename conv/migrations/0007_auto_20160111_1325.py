# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0006_auto_20160108_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='ronde',
            field=models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3)], verbose_name='Ronde'),
            preserve_default=False,
        ),
    ]
