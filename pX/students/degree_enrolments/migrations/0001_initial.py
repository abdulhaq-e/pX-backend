# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('periods', '0001_initial'),
        ('degrees', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DegreeEnrolment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('degree_enrolment_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('enrolment_id', models.UUIDField()),
                ('enrolment_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DegreeMajorEnrolment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('degree_major_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('degree', models.ForeignKey(to='degrees.Degree')),
                ('period', models.ForeignKey(to='periods.Period')),
                ('previous_degree', models.ForeignKey(related_name='majored_students', on_delete=django.db.models.deletion.PROTECT, to='degrees.Degree')),
                ('student', models.ForeignKey(to='students.Student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DegreeOriginalEnrolment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('degree_original_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('degree', models.ForeignKey(to='degrees.Degree')),
                ('period', models.ForeignKey(to='periods.Period')),
                ('student', models.ForeignKey(to='students.Student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DegreeTransfer',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('degree_transfer_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('degree', models.ForeignKey(to='degrees.Degree')),
                ('period', models.ForeignKey(to='periods.Period')),
                ('previous_degree', models.ForeignKey(related_name='previous_students', on_delete=django.db.models.deletion.PROTECT, to='degrees.Degree')),
                ('student', models.ForeignKey(to='students.Student')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
