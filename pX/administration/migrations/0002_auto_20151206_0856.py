# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='acronym',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='department',
            name='acronym_ar',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='acronym_en',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
