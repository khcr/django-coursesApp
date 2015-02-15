# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20150207_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progression',
            name='page',
            field=models.OneToOneField(to='courses.Page'),
        ),
    ]
