from django.db import models
from django.contrib.auth.models import User

#
#  Classification
#
class Theme(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
      return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=50)

    theme = models.ForeignKey(Theme, related_name="chapters")

    def __str__(self):
      return self.name

#
# Status progressions
#
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#
# Course build
#
class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200)
    difficulty = models.IntegerField()
    published = models.BooleanField(default=False)
    
    author = models.ForeignKey(User, related_name="courses")
    chapter = models.ForeignKey(Chapter, related_name="courses")
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

    def percentage(self):
        done = self.pages.filter(progression__status__name="Compris").count()
        percentage = done / self.total_pages() * 100
        return round(percentage/5) * 5

    def has_favorite(self, user):
        return user in self.favorites.all()


class Page(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()
    
    course = models.ForeignKey(Course, related_name="pages")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
      return self.name

    def state(self, user):
        try:
            progession = self.progression_set.get(user=user)
        except Progression.DoesNotExist:
            return None
        else:
            return progession.status.name

class Section(models.Model):
    name = models.CharField(max_length=50)
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
    content = models.TextField(max_length=300)
    
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Progression(models.Model):
    page = models.ForeignKey(Page)
    status = models.ForeignKey(Status)
    user = models.ForeignKey(User)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "status: {}, page: {}".format(self.status.name, self.page.name)

#
# Méthodes d'utilisateurs
#

def is_teacher(self):
    return self.groups.filter(name="Teacher").exists()

User.add_to_class('is_teacher', is_teacher)