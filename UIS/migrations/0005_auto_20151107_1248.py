# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0004_auto_20151107_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='previous_warnings',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='warnings',
            field=models.IntegerField(),
        ),
    ]
