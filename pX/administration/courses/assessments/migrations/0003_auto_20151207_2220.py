# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0002_assessmentresult_section_enrolment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='period_course',
            field=models.ForeignKey(related_name='assessments', on_delete=django.db.models.deletion.PROTECT, to='courses.PeriodCourse'),
        ),
    ]
