# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0004_auto_20150903_1813'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAllowedEnrolments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('permitted', models.BooleanField(default=True)),
                ('primary', models.BooleanField(default=True)),
                ('period_course', models.ForeignKey(to='UIS.PeriodCourse')),
                ('student', models.ForeignKey(to='UIS.Student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisites',
            field=models.ManyToManyField(related_name='required_for', through='UIS.CoursePrerequisite', to='UIS.Course', blank=True),
        ),
    ]
