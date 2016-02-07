# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '__first__'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('details', models.OneToOneField(parent_link=True, to='users.Person')),
                ('registration_number', models.CharField(unique=True, max_length=255, verbose_name='Student UUID')),
                ('status', models.CharField(default='E', max_length=1, choices=[('E', 'Enrolled'), ('G', 'Graduated'), ('L', 'Left'), ('D', 'Dropped Out'), ('T', 'Transferred'), ('K', 'Kicked Out')])),
                ('advisor', models.CharField(max_length=200, null=True, blank=True)),
            ],
            bases=('users.person',),
        ),
        migrations.CreateModel(
            name='StudentAllowedEnrolment',
            fields=[
                ('student_allowed_enrolments_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('course', models.ForeignKey(to='courses.Course')),
                ('student', models.ForeignKey(related_name='allowed_enrolment', to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('student_results_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('period_count', models.IntegerField()),
                ('actual_period_count', models.IntegerField()),
                ('registered_credits', models.FloatField()),
                ('passed_credits', models.FloatField()),
                ('repeated_credits', models.FloatField()),
                ('cumulative_registered_credits', models.FloatField()),
                ('cumulative_passed_credits', models.FloatField()),
                ('scored_points', models.FloatField()),
                ('passed_points', models.FloatField()),
                ('repeated_points', models.FloatField()),
                ('cumulative_scored_points', models.FloatField()),
                ('GPA', models.FloatField()),
                ('cumulative_GPA', models.FloatField()),
                ('previous_GPA', models.FloatField()),
                ('warnings', models.IntegerField()),
                ('previous_warnings', models.IntegerField()),
                ('very_poor_warnings', models.IntegerField(default=0)),
                ('expulsion', models.IntegerField(default=False)),
            ],
        ),
    ]
