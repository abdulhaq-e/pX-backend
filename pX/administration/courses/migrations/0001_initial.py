# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('degrees', '0001_initial'),
        ('administration', '0001_initial'),
        ('periods', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('course_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('code', models.CharField(max_length=20)),
                ('level', models.SmallIntegerField(null=True)),
                ('name', models.CharField(max_length=200, verbose_name='Course name', blank=True)),
                ('name_en', models.CharField(max_length=200, null=True, verbose_name='Course name', blank=True)),
                ('name_ar', models.CharField(max_length=200, null=True, verbose_name='Course name', blank=True)),
                ('is_obsolete', models.BooleanField(default=False)),
                ('credit', models.SmallIntegerField()),
                ('course_description', models.TextField(blank=True)),
                ('course_description_en', models.TextField(null=True, blank=True)),
                ('course_description_ar', models.TextField(null=True, blank=True)),
                ('course_syllabus', models.TextField(blank=True)),
                ('course_syllabus_en', models.TextField(null=True, blank=True)),
                ('course_syllabus_ar', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['level', 'code'],
                'verbose_name': 'Course Catalogue',
                'verbose_name_plural': 'Course Catalogue',
            },
        ),
        migrations.CreateModel(
            name='CoursePrerequisite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('course', models.ForeignKey(related_name='prerequisites', to='courses.Course')),
                ('prerequisite', models.ForeignKey(related_name='required_for', to='courses.Course')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DegreeCourse',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('degree_course_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='courses.Course')),
                ('degree', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='degrees.Degree')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodCourse',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('period_course_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('shared_groups', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='courses.Course')),
                ('period', models.ForeignKey(to='periods.Period')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodCourseSubSection',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('period_course_section_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('is_compulsary', models.BooleanField(default=True)),
                ('period_course', models.ForeignKey(to='courses.PeriodCourse')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('section_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=15, blank=True)),
                ('name_en', models.CharField(max_length=15, null=True, blank=True)),
                ('name_ar', models.CharField(max_length=15, null=True, blank=True)),
                ('group', models.CharField(max_length=10, null=True, blank=True)),
                ('period_course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='courses.PeriodCourse')),
            ],
        ),
        migrations.CreateModel(
            name='SubSection',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('sub_section_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=15, blank=True)),
                ('group', models.CharField(max_length=10, null=True, blank=True)),
                ('section_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='courses.PeriodCourseSubSection')),
            ],
        ),
        migrations.CreateModel(
            name='SubSectionType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('section_type_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('name_en', models.CharField(max_length=40, null=True)),
                ('name_ar', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='periodcoursesubsection',
            name='section_type',
            field=models.ForeignKey(to='courses.SubSectionType'),
        ),
        migrations.AddField(
            model_name='periodcourse',
            name='section_types',
            field=models.ManyToManyField(to='courses.SubSectionType', through='courses.PeriodCourseSubSection'),
        ),
        migrations.AddField(
            model_name='course',
            name='degrees',
            field=models.ManyToManyField(related_name='courses', through='courses.DegreeCourse', to='degrees.Degree', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='administration.Department'),
        ),
        migrations.AddField(
            model_name='course',
            name='equalled_courses',
            field=models.ManyToManyField(related_name='equalled_with', to='courses.Course', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='periods',
            field=models.ManyToManyField(related_name='available_periods', through='courses.PeriodCourse', to='courses.Course', blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='prerequisite_courses',
            field=models.ManyToManyField(to='courses.Course', through='courses.CoursePrerequisite', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='subsection',
            unique_together=set([('section_type', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('period_course', 'group')]),
        ),
        migrations.AlterUniqueTogether(
            name='periodcourse',
            unique_together=set([('period', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='degreecourse',
            unique_together=set([('course', 'degree')]),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('code', 'name', 'department', 'credit')]),
        ),
    ]
