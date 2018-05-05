# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0014_auto_20180303_0129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='editions',
            field=models.ManyToManyField(db_constraint='Editions this user attendented', to='conv.Edition'),
        ),
    ]
