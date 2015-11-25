# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0003_auto_20151107_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresult',
            name='previous_warnings',
            field=models.IntegerField(default=10000),
        ),
        migrations.AddField(
            model_name='studentresult',
            name='warnings',
            field=models.IntegerField(default=10000),
        ),
    ]
