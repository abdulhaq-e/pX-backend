# -*- coding: utf-8 -*-
# Generated by Django 1.9.1.dev20151224150756 on 2016-01-11 16:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0005_auto_20151218_2040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assessment',
            options={},
        ),
        migrations.AlterModelOptions(
            name='assessmentresult',
            options={},
        ),
        migrations.AlterField(
            model_name='assessmentresult',
            name='section_enrolment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_results', to='section_enrolments.SectionEnrolment'),
        ),
        migrations.AlterUniqueTogether(
            name='assessment',
            unique_together=set([('assessment_type', 'period_course')]),
        ),
        migrations.AlterUniqueTogether(
            name='assessmentresult',
            unique_together=set([('assessment', 'section_enrolment')]),
        ),
    ]
