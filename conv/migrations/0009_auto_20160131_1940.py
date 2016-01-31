# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0008_auto_20160112_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ronde',
            field=models.IntegerField(verbose_name='Ronde', choices=[(1, '1 : Samedi 14h−20h'), (2, '2 : Samedi à partir de 20h'), (3, '3 : Dimanche 10h-16h')]),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='ronde',
            field=models.IntegerField(verbose_name='Ronde', choices=[(1, '1 : Samedi 14h−20h'), (2, '2 : Samedi à partir de 20h'), (3, '3 : Dimanche 10h-16h')]),
        ),
    ]
