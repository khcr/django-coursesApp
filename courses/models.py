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
# Statuts
#
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

#
# Cours
#
class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200)
    difficulty = models.IntegerField()
    published = models.BooleanField(default=False)
    
    author = models.ForeignKey(User, related_name="courses")
    chapter = models.ForeignKey(Chapter, related_name="courses")
    favorites = models.ManyToManyField(User, related_name="favorite_courses", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return self.name

    # retourne le nombre total de pages du cours
    def total_pages(self):
        return self.pages.count()

    # calcule le pourcentage lu du cours en fonction de la progression et du nombre total de pages
    def percentage(self, user):
        # pages marquées comme "comprises"
        done = self.pages.filter(progression__user_id=user.id, progression__status__name="Compris").count()
        # pourcentage
        percentage = done / self.total_pages() * 100
        # arrondit le pourcentage
        return round(percentage/5) * 5

    # retourne si le cours fait parti des favoris d'un utilisateur
    def has_favorite(self, user):
        return user in self.favorites.all()


class Page(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField()
    
    course = models.ForeignKey(Course, related_name="pages")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Par défaut, retourne les pages triées par la colonne "order"
        ordering = ['order']

    def __str__(self):
      return self.name

    # retourne le statut d'une page pour un utilisateur
    # Par exemple "Compris" ou "Relire"
    def state(self, user):
        try:
            progession = self.progression_set.get(user=user)
        except Progression.DoesNotExist:
            return None
        else:
            return progession.status.name

class Section(models.Model):
    name = models.CharField(max_length=50)
    # contient le texte du cours en Markdown
    markdown_content = models.TextField(default="")
    # contient le texte du cours en HTML
    html_content = models.TextField(blank=True)
    order = models.IntegerField()
    
    page = models.ForeignKey(Page, related_name="sections")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Par défaut, retourne les sections triées par la colonne "order"
        ordering = ['order']

    def __str__(self):
      return self.name

#
# Fonctionnalités pour les utilisateurs
#

# Commentaires des cours
class CourseComment(models.Model):
    content = models.TextField(max_length=300)
    
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Progression dans un cours
class Progression(models.Model):
    page = models.ForeignKey(Page)
    status = models.ForeignKey(Status)
    user = models.ForeignKey(User)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "status: {}, page: {}".format(self.status.name, self.page.name)

#
# Méthodes ajoutées au modèle User
#

# teste si l'utilisateur est un professeur
def is_teacher(self):
    return self.groups.filter(name="Teacher").exists()

User.add_to_class('is_teacher', is_teacher)