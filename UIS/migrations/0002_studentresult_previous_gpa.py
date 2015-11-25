# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresult',
            name='previous_GPA',
            field=models.FloatField(default=-1.1),
        ),
    ]
