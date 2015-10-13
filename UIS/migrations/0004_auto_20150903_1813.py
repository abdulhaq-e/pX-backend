# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UIS', '0003_auto_20150903_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentregistration',
            name='student',
            field=models.ForeignKey(related_name='student_registrations', verbose_name='student', to='UIS.Student'),
        ),
    ]
