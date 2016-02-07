# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('name', models.CharField(unique=True, max_length=60, verbose_name='Name of Faculty')),
                ('name_en', models.CharField(max_length=60, unique=True, null=True, verbose_name='Name of Faculty')),
                ('name_ar', models.CharField(max_length=60, unique=True, null=True, verbose_name='Name of Faculty')),
                ('acronym', models.CharField(max_length=3)),
                ('acronym_en', models.CharField(max_length=3, null=True)),
                ('acronym_ar', models.CharField(max_length=3, null=True)),
                ('domain_name', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('name', models.CharField(unique=True, max_length=60, verbose_name='Name of Faculty')),
                ('name_en', models.CharField(max_length=60, unique=True, null=True, verbose_name='Name of Faculty')),
                ('name_ar', models.CharField(max_length=60, unique=True, null=True, verbose_name='Name of Faculty')),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(to='administration.Faculty', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
