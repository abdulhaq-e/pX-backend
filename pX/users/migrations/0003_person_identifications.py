# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identifications', '0001_initial'),
        ('users', '0002_pxuser_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='identifications',
            field=models.ManyToManyField(to='identifications.Identification', through='identifications.PersonID'),
        ),
    ]
