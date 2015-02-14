# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20150205_2149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'ordering': ['order']},
        ),
    ]
