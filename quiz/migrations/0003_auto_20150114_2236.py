# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_student'),
        ('quiz', '0002_completedquiz_qcm_qcmchoice_qcmsubmit_quiz_simplequestion_sqanswer_sqsubmit'),
        ('teachers', '0002_auto_20150114_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='id_chapter',
            field=models.ForeignKey(to='teachers.Chapter'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quiz',
            name='id_prof',
            field=models.ForeignKey(to='teachers.Teacher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='qcmsubmit',
            name='submitted_quiz',
            field=models.ForeignKey(to='quiz.CompletedQuiz'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='qcm',
            name='id_quiz',
            field=models.ForeignKey(to='quiz.Quiz'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedquiz',
            name='id_quiz',
            field=models.ForeignKey(to='quiz.Quiz'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='completedquiz',
            name='id_student',
            field=models.ForeignKey(to='students.Student'),
            preserve_default=True,
        ),
    ]
