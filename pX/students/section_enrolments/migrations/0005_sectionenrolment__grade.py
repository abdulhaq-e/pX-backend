# -*- coding: utf-8 -*-
# Generated by Django 1.9.2.dev20160111111649 on 2016-01-12 00:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section_enrolments', '0004_auto_20160111_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='sectionenrolment',
            name='_grade',
            field=models.FloatField(null=True),
        ),
    ]
