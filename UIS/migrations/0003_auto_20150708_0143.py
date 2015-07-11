# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import UIS.validators


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0002_auto_20150704_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentenrolment',
            name='carry_marks',
            field=models.FloatField(blank=True, null=True, validators=[UIS.validators.validate_grade]),
        ),
        migrations.AddField(
            model_name='studentenrolment',
            name='final_exam',
            field=models.FloatField(blank=True, null=True, validators=[UIS.validators.validate_grade]),
        ),
    ]
