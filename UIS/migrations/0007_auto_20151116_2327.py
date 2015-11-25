# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0006_auto_20151116_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='very_poor_warnings',
            field=models.IntegerField(default=0),
        ),
    ]
