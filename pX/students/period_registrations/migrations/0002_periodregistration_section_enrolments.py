# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section_enrolments', '0001_initial'),
        ('courses', '0001_initial'),
        ('period_registrations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodregistration',
            name='section_enrolments',
            field=models.ManyToManyField(to='courses.Section', through='section_enrolments.SectionEnrolment', blank=True),
        ),
    ]
