# -*- coding: utf-8 -*-
# Generated by Django 1.9.2.dev20160111111649 on 2016-01-11 23:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('period_registrations', '0002_periodregistration_section_enrolments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodregistration',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='period_registrations', to='students.Student', verbose_name='student'),
        ),
    ]
