# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0010_auto_20150914_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='advisor',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
