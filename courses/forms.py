from django.forms import ModelForm

from courses.models import Course, Page, Section
from teachers.models import Teacher

# Create the form class.
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'chapter', 'difficulty']

class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['name']

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'html_content', 'markdown_content', 'order', 'page']