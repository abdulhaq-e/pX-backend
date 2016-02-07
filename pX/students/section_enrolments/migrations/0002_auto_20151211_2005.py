# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section_enrolments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sectionenrolment',
            options={'ordering': ('period_registration',)},
        ),
        migrations.RenameField(
            model_name='sectionenrolment',
            old_name='student_registration',
            new_name='period_registration',
        ),
        migrations.AlterField(
            model_name='sectionenrolment',
            name='sub_sections',
            field=models.ManyToManyField(to='courses.SubSection', through='section_enrolments.SubSectionEnrolment', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='sectionenrolment',
            unique_together=set([('period_registration', 'section')]),
        ),
    ]
