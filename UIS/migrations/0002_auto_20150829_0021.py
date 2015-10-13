# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('code', 'name_ar', 'department', 'credit'), ('code', 'name', 'department', 'credit')]),
        ),
        migrations.RemoveField(
            model_name='course',
            name='first_taught',
        ),
        migrations.RemoveField(
            model_name='course',
            name='is_compulsary',
        ),
        migrations.RemoveField(
            model_name='course',
            name='last_tught',
        ),
    ]
