# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_auto_20151206_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='periods',
            field=models.ManyToManyField(related_name='students', through='period_registrations.PeriodRegistration', to='periods.Period', blank=True),
        ),
    ]
