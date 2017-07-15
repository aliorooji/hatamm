# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Charity', '0015_auto_20170608_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helperprofile',
            name='monthly_cooperation_time',
            field=models.IntegerField(null=True, blank=True, verbose_name='حد اقل زمان همکاری در ماه'),
        ),
    ]
