from django.db import models

# Create your models here.

class Quiz(models.Model): #Infos générales sur le quiz
    title = models.CharField(max_length=100)
    creation_date = models.DateField()
    code = models.CharField(max_length=1000) #Format texte du quiz
    id_prof = models.ForeignKey('teachers.Teacher')
    id_chapter = models.ForeignKey('teachers.Chapter')
    
class CompletedQuiz(models.Model): #Tentative de réponse au quiz par un élève
    submit_date = models.DateField()
    id_quiz = models.ForeignKey(Quiz) #Relation avec le quiz complété
    id_student = models.ForeignKey('students.Student')

#    
#Classes abstraites
#

class QuizQuestion(models.Model): #Classe abstraite dont héritent toutes les questions
    text = models.CharField(max_length=200) #Énoncé
    comment = models.CharField(max_length=200) #Commentaire affiché lors de la correction
    number = models.IntegerField() #Ordre de la question dans le quiz
    id_quiz = models.ForeignKey(Quiz)
    
    class Meta:
        abstract = True

#
#Tables concernant les questions simples
#
        
class SimpleQuestion(QuizQuestion):
    pass

class SqAnswer(models.Model): #Les réponses correctes
    text = models.CharField(max_length=50)
    question = models.ForeignKey(SimpleQuestion) #Relation vers la question

class SqSubmit(models.Model): #Réponse soumise par un élève
    text = models.CharField(max_length=50)
    question = models.ForeignKey(SimpleQuestion) #Relation vers la question à laquelle l'élève a répondu
    submitted_quiz = models.ForeignKey(CompletedQuiz) #Relation vers la tentative

#    
#Tables concernant les QCM
#

class Qcm(QuizQuestion):
    multi_answers = models.BooleanField() #True si il est possible de cocher plusieurs choix
    show_list = models.BooleanField() #True si les choix sont affichés sous forme de liste déroulante
    
class QcmChoice(models.Model): #Choix affichés pour un QCM
    text = models.CharField(max_length=50)
    valid = models.BooleanField() #Vaut True si la case doit être cochée
        
class QcmSubmit(models.Model): #Choix sélectionnés par l'élève dans un QCM
    submitted_quiz = models.ForeignKey(CompletedQuiz) #Relation vers la tentative