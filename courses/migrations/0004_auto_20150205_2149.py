# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20150114_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecomment',
            name='section',
            field=models.ForeignKey(to='courses.Section', null=True),
        ),
    ]
