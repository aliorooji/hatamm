# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NotAndBlog', '0004_auto_20170524_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='n_type',
            field=models.CharField(max_length=10, choices=[('p_i_p', 'پست موسسه درباره پروژه'), ('p_ha', ''), ('p_he', ''), ('r_ha', ''), ('r_he', 'گزارش مددکار توسط موسسه'), ('r_i', ''), ('n_ha_i', ''), ('n_ha_he', ''), ('n_i_ha', ''), ('n_i_he', ''), ('n_he_i', ''), ('n_he_ha', '')], default=None, verbose_name='نوع'),
        ),
    ]
