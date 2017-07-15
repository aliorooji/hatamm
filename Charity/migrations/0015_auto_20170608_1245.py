# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Charity', '0014_auto_20170608_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='n_score',
            field=models.IntegerField(default=None, null=True, blank=True, verbose_name='امتیاز منفی'),
        ),
    ]
