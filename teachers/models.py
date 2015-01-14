from django.db import models
from django.contrib.auth.models import User

class Teacher(User):
    pass

class Group(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ManyToManyField(Teacher)
    student = models.ManyToManyField('students.Student')
    
#
#  Classification
#
class Theme(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
      return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=30)

    theme = models.ForeignKey(Theme, related_name="chapters")

    def __str__(self):
      return self.name