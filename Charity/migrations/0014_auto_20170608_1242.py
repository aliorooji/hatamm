# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Charity', '0013_auto_20170530_0826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='father',
        ),
        migrations.RemoveField(
            model_name='manytomany',
            name='cities_wants_to_go',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
