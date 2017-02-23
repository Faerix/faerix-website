# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0011_auto_20170104_0353'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='conv',
            field=models.ForeignKey(to='conv.Edition', default=2016, related_name='sponsor_conv'),
            preserve_default=False,
        ),
    ]
