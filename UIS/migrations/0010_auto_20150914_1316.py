# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0009_studentallowedenrolments'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAllowedEnrolment',
            fields=[
                ('student_allowed_enrolments_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('course', models.ForeignKey(to='UIS.Course')),
                ('student', models.ForeignKey(related_name='allowed_enrolment', to='UIS.Student')),
            ],
        ),
        migrations.RemoveField(
            model_name='studentallowedenrolments',
            name='course',
        ),
        migrations.RemoveField(
            model_name='studentallowedenrolments',
            name='student',
        ),
        migrations.DeleteModel(
            name='StudentAllowedEnrolments',
        ),
    ]
