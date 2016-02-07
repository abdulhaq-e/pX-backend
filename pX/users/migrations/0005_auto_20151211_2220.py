# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20151211_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='identifications',
            field=models.ManyToManyField(to='identifications.Identification', through='identifications.PersonID', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='nationality',
            field=django_countries.fields.CountryField(default='LY', max_length=2),
        ),
    ]
