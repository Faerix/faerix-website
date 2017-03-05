# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('conv', '0010_auto_20170114_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='conv',
            field=models.ForeignKey(to='conv.Edition', related_name='sponsor_conv', default=2017),
            preserve_default=False,
        ),
    ]
