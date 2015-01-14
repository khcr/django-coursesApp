# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0002_correction_exercise_exercise_type_skill'),
        ('auth', '0001_initial'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True, parent_link=True)),
                ('done_skills', models.ManyToManyField(to='exercises.Skill')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
        ),
    ]
