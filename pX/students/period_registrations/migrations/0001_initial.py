# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('periods', '0001_initial'),
        #('section_enrolments', '__first__'),
        ('courses', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodRegistration',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('student_registration_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('registration_type', models.CharField(default='RNC', max_length=3, choices=[('Suspended', (('DS', 'Disciplinary Suspension '), ('ES', 'Exceptional Suspension'), ('NS', 'Normal Suspension'))), ('R', 'Registered'), ('D', 'Dropped Out'), ('RNC', 'Registration not completed')])),
                #('enrolments', models.ManyToManyField(to='courses.Section', through='section_enrolments.SectionEnrolment', blank=True)),
                ('period', models.ForeignKey(to='periods.Period')),
                ('student', models.ForeignKey(related_name='student_registrations', verbose_name='student', to='students.Student')),
            ],
            options={
                'ordering': ('student', 'period'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='periodregistration',
            unique_together=set([('student', 'period')]),
        ),
    ]
