# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0008_auto_20150914_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAllowedEnrolments',
            fields=[
                ('student_allowed_enrolments_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('course', models.ForeignKey(to='UIS.Course')),
                ('student', models.ForeignKey(to='UIS.Student')),
            ],
        ),
    ]
