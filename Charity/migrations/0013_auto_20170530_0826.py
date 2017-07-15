# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Charity', '0012_auto_20170529_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helperprofile',
            name='tag2',
        ),
        migrations.RemoveField(
            model_name='helperprofile',
            name='tag3',
        ),
        migrations.RemoveField(
            model_name='institute',
            name='tag3',
        ),
        migrations.RemoveField(
            model_name='institute',
            name='tag4',
        ),
        migrations.AddField(
            model_name='helperprofile',
            name='city',
            field=models.CharField(null=True, max_length=20, default=None, verbose_name='شهر', blank=True),
        ),
        migrations.AddField(
            model_name='helperprofile',
            name='province',
            field=models.CharField(null=True, max_length=20, default=None, verbose_name='استان', blank=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='city',
            field=models.CharField(null=True, max_length=20, default=None, verbose_name='شهر', blank=True),
        ),
        migrations.AddField(
            model_name='institute',
            name='province',
            field=models.CharField(null=True, max_length=20, default=None, verbose_name='استان', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='city',
            field=models.CharField(null=True, max_length=20, default=None, verbose_name='شهر', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='province',
            field=models.CharField(null=True, max_length=20, default=None, verbose_name='استان', blank=True),
        ),
    ]
