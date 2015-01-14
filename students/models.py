from django.db import models
from django.contrib.auth.models import User

class Student(User):
    done_skills = models.ManyToManyField('exercises.Skill')
    
    def __str__(self):
        return '%s %s' % (self.prenom, self.nom)