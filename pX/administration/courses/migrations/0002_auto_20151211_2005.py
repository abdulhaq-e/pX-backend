# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='group',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='period_course',
            field=models.ForeignKey(to='courses.PeriodCourse', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
