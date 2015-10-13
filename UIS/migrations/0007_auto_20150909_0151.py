# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0006_auto_20150909_0149'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoursePrerequisite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('course', models.ForeignKey(related_name='prerequisites', to='UIS.Course')),
                ('prerequisite', models.ForeignKey(related_name='required_for', to='UIS.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisite_courses',
            field=models.ManyToManyField(to='UIS.Course', through='UIS.CoursePrerequisite', blank=True),
        ),
    ]
