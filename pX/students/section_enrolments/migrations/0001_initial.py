# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('period_registrations', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionEnrolment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('section_enrolment_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('section', models.ForeignKey(related_name='studentenrolment', on_delete=django.db.models.deletion.PROTECT, to='courses.Section')),
                ('student_registration', models.ForeignKey(related_name='studentenrolment', on_delete=django.db.models.deletion.PROTECT, to='period_registrations.PeriodRegistration')),
            ],
            options={
                'ordering': ('student_registration',),
            },
        ),
        migrations.CreateModel(
            name='SectionEnrolmentLog',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('section_enrolment_log_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('enrolment_status', models.CharField(default='A', max_length=1, choices=[('A', 'Added'), ('D', 'Dropped')])),
                ('section', models.ForeignKey(related_name='studentenrolmentlog', on_delete=django.db.models.deletion.PROTECT, to='courses.Section')),
                ('student_registration', models.ForeignKey(related_name='studentenrolmentlog', on_delete=django.db.models.deletion.PROTECT, to='period_registrations.PeriodRegistration')),
            ],
        ),
        migrations.CreateModel(
            name='SubSectionEnrolment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('enrolment', models.ForeignKey(to='section_enrolments.SectionEnrolment')),
                ('sub_section', models.ForeignKey(to='courses.SubSection', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='sectionenrolment',
            name='sub_sections',
            field=models.ManyToManyField(to='courses.SubSection', through='section_enrolments.SubSectionEnrolment'),
        ),
        migrations.AlterUniqueTogether(
            name='sectionenrolmentlog',
            unique_together=set([('student_registration', 'section', 'enrolment_status')]),
        ),
        migrations.AlterUniqueTogether(
            name='sectionenrolment',
            unique_together=set([('student_registration', 'section')]),
        ),
    ]
