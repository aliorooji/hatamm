# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Charity', '0011_auto_20170522_1849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manytomany',
            options={'verbose_name': 'روابط', 'verbose_name_plural': 'روابط'},
        ),
        migrations.RenameField(
            model_name='project',
            old_name='tag5',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='tag6',
            new_name='province',
        ),
    ]
