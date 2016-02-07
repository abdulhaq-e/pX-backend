# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        #('section_enrolments', '__first__'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('assessment_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('total_grade', models.FloatField()),
                ('result_status', models.CharField(default='U', max_length=1, choices=[('U', 'Unpublished'), ('P', 'Published'), ('O', 'On hold')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentResult',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('assessment_grade_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('grade', models.FloatField(null=True)),
                ('hidden', models.BooleanField(default=False)),
                ('assessment', models.ForeignKey(to='assessments.Assessment')),
                #('student_enrolment', models.ForeignKey(to='section_enrolments.SectionEnrolment')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AssessmentType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('assessment_type_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('assessment_type', models.CharField(max_length=100)),
                ('assessment_type_en', models.CharField(max_length=100, null=True)),
                ('assessment_type_ar', models.CharField(max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='assessment',
            name='assessment_type',
            field=models.ForeignKey(to='assessments.AssessmentType', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='assessment',
            name='period_course',
            field=models.ForeignKey(to='courses.PeriodCourse', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
