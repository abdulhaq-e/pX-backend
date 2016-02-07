# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pxuser',
            name='roles',
            field=models.ManyToManyField(to='roles.Role', through='roles.UserRole'),
        ),
    ]
