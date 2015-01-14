from django.db import models
from django.contrib.auth.models import User

#
# Status progressions
#
class Status(models.Model):
    name = models.CharField(max_length=30, unique=True)

#
# Course build
#
class Course(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    difficulty = models.IntegerField()
    
    author = models.ForeignKey('teachers.Teacher', related_name="courses")
    chapter = models.ForeignKey('teachers.Chapter', related_name="courses")
    favorites = models.ManyToManyField(User, related_name="favorite_courses", blank=True, null=True)
    # videos = models.ManyToManyField(Video)
    # images = models.ManyToManyField(Image)
    # definitions = models.ManyToManyField(Definition)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return self.name

    def total_pages(self):
        return self.pages.count()


class Page(models.Model):
    name = models.CharField(max_length=30)
    order = models.IntegerField()
    
    course = models.ForeignKey(Course, related_name="pages")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return self.name

class Section(models.Model):
    name = models.CharField(max_length=30)
    markdown_content = models.TextField(default="")
    html_content = models.TextField(blank=True)
    order = models.IntegerField()
    
    page = models.ForeignKey(Page, related_name="sections")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
      return self.name

#
# User functionalities
#
class CourseComment(models.Model):
    content = models.TextField()
    
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    section = models.ForeignKey(Section)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CourseRequest(models.Model):
    name = models.CharField(max_length=30)
    content = models.TextField()
    
    user = models.ForeignKey(User)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Progression(models.Model):
    page = models.ForeignKey(Page)
    status = models.ForeignKey(Status)
    user = models.ForeignKey(User)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#
# Various
#
class Definition(models.Model):
    word = models.CharField(max_length=20)
    definition = models.TextField()

class Video(models.Model):

    def filename(instance, filename):
        return "/courses/static/courses/uploads/videos/{}/{}".format(instance.pk, filename)

    video = models.FileField(upload_to=filename)

class Image(models.Model):

    def filename(instance, filename):
        return "/courses/static/courses/uploads/images/{}/{}".format(instance.pk, filename)

    image = models.ImageField(upload_to=filename)
