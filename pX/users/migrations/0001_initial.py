# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django_countries.fields
import django.db.models.deletion
from django.conf import settings
import pX.users.managers
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('administration', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='pXUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('user_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', pX.users.managers.pXUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('person_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('first_name_en', models.CharField(max_length=50, null=True, verbose_name='first name')),
                ('first_name_ar', models.CharField(max_length=50, null=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last Name')),
                ('last_name_en', models.CharField(max_length=50, null=True, verbose_name='last Name')),
                ('last_name_ar', models.CharField(max_length=50, null=True, verbose_name='last Name')),
                ('date_of_birth', models.DateField(null=True)),
                ('gender', models.CharField(max_length=1, null=True, choices=[('M', 'Male'), ('F', 'Female')])),
                ('nationality', django_countries.fields.CountryField(default='LY', max_length=2, null=True)),
                ('address', models.CharField(max_length=45, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
                ('user_profile_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('profile_id', models.UUIDField()),
                ('profile_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('details', models.OneToOneField(parent_link=True, to='users.Person')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')])),
                ('department', models.ForeignKey(to='administration.Department', on_delete=django.db.models.deletion.PROTECT)),
            ],
            bases=('users.person',),
        ),
        migrations.AlterUniqueTogether(
            name='employee',
            unique_together=set([('username', 'department')]),
        ),
    ]
