# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0002_auto_20150829_0021'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentenrolment',
            options={'ordering': ('student_registration',)},
        ),
        migrations.AlterField(
            model_name='studentregistration',
            name='student',
            field=models.ForeignKey(related_name='student_registration', verbose_name='student', to='UIS.Student'),
        ),
    ]
