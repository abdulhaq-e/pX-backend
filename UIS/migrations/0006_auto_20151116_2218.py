# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0005_auto_20151107_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresult',
            name='expulsion',
            field=models.IntegerField(default=False),
        ),
        migrations.AddField(
            model_name='studentresult',
            name='very_poor_warnings',
            field=models.IntegerField(default=100000),
        ),
    ]
