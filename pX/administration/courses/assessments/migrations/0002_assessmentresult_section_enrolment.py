# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section_enrolments', '0001_initial'),
        ('assessments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentresult',
            name='section_enrolment',
            field=models.ForeignKey(to='section_enrolments.SectionEnrolment'),
            preserve_default=False,
        ),
    ]
