# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0002_auto_20150114_2236'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_auto_20150114_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='author',
            field=models.ForeignKey(related_name='courses', to='teachers.Teacher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='chapter',
            field=models.ForeignKey(related_name='courses', to='teachers.Chapter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='favorites',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True, related_name='favorite_courses', null=True),
            preserve_default=True,
        ),
    ]
