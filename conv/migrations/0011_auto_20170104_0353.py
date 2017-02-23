# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0010_auto_20170104_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='conv',
            field=models.ForeignKey(default=2017, to='conv.Edition', related_name='even_conv'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scenario',
            name='conv',
            field=models.ForeignKey(default=2017, to='conv.Edition', related_name='conv'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='editions',
            field=models.ManyToManyField(db_constraint='Editions this user attendented', to='conv.Edition'),
        ),
    ]
