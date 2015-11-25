# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0002_studentresult_previous_gpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='previous_GPA',
            field=models.FloatField(),
        ),
    ]
