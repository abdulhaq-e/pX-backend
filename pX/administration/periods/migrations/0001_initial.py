# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid
import exclusivebooleanfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('period_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('academic_year', models.CommaSeparatedIntegerField(help_text='please enter the academic year in this format:         for the year 2012-2013, enter: "2012,2013" (without quotes)', max_length=9, verbose_name='academic year')),
                ('period', models.IntegerField(choices=[(0, 'Academic Year'), (1, 'Autumn'), (2, 'Spring'), (3, 'Summer')])),
                ('set_current_period', exclusivebooleanfield.fields.ExclusiveBooleanField(default=True)),
            ],
            options={
                'ordering': ['academic_year', 'period'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='period',
            unique_together=set([('academic_year', 'period')]),
        ),
    ]
