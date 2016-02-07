# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0003_auto_20151207_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessmenttype',
            name='assessment_type',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='assessmenttype',
            name='assessment_type_ar',
            field=models.CharField(max_length=100, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='assessmenttype',
            name='assessment_type_en',
            field=models.CharField(max_length=100, unique=True, null=True),
        ),
    ]
