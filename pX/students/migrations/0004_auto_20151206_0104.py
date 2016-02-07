# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_studentresult_period_registration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentresult',
            options={'ordering': ('period_registration',)},
        ),
    ]
