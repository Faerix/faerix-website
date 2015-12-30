# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0002_auto_20151230_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='ronde',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], blank=True, null=True),
        ),
    ]
