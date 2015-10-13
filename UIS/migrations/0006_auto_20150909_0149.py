# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0005_auto_20150908_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseprerequisite',
            name='course',
        ),
        migrations.RemoveField(
            model_name='course',
            name='prerequisites',
        ),
        migrations.DeleteModel(
            name='CoursePrerequisite',
        ),
    ]
