# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
        ('periods', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('degree_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('level', models.CharField(max_length=1, choices=[(b'U', 'Undergraduate'), (b'P', 'Postgraduate')])),
                ('name', models.CharField(max_length=60)),
                ('name_en', models.CharField(max_length=60, null=True)),
                ('name_ar', models.CharField(max_length=60, null=True)),
                ('credits_required', models.SmallIntegerField()),
                ('is_major', models.BooleanField(default=True)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='administration.Department')),
                ('minors', models.ManyToManyField(related_name='_degree_minors_+', to='degrees.Degree', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodDegree',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('period_degree_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('is_compulsary', models.BooleanField(default=True)),
                ('degree', models.ForeignKey(to='degrees.Degree', on_delete=django.db.models.deletion.PROTECT)),
                ('period', models.ForeignKey(to='periods.Period', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.AddField(
            model_name='degree',
            name='periods',
            field=models.ManyToManyField(to='periods.Period', through='degrees.PeriodDegree', blank=True),
        ),
        migrations.AddField(
            model_name='degree',
            name='replaced_degrees',
            field=models.ManyToManyField(related_name='_degree_replaced_degrees_+', to='degrees.Degree', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='perioddegree',
            unique_together=set([('period', 'degree')]),
        ),
        migrations.AlterUniqueTogether(
            name='degree',
            unique_together=set([('name', 'credits_required', 'department')]),
        ),
    ]
