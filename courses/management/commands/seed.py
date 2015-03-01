from django.core.management.base import BaseCommand
from courses.models import *
from teachers.models import *
from courses.utils import clear_tables
import os

class Command(BaseCommand):
    help = 'Create demo data for testing'

    def handle(self, *args, **options):
        clear_tables([Theme, Chapter, Teacher, Status, Course, Page, Section, Progression, CourseComment])
        # Chapters & Themes
        theme = Theme(name="Géométrie")
        theme.save()
        chapter = Chapter(theme=theme, name="Les droites")
        chapter.save()
        # Teacher
        teacher = Teacher(first_name="John", last_name="Smith", email="john@smith.com", username="sjohn")
        teacher.save()
        # Status
        Status(name="Compris").save()
        Status(name="Relire").save()
        # Demo course
        course = Course(name="Equations de droites", 
            description="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit",
            difficulty=1,
            author=teacher,
            chapter=chapter,
            published=True
            )
        course.save()
        page_1 = Page(name="Généralité", course=course, order=1)
        page_1.save()
        text_1 = """In a quam felis. Mauris varius at nulla sed egestas. Quisque tempus nisi quis libero interdum iaculis. Cras vel euismod ante, 
        ut eleifend nibh. || x\ =\ \\frac{\sqrt{144}}{2}\ \\times\ (y\ +\ 12) || Aenean interdum vulputate lorem, non elementum leo placerat vel. 
        Aenean luctus felis eu ligula luctus, at efficitur ligula mattis. Nam erat lectus, interdum eget volutpat eget, semper ut sem. 
        Pellentesque pretium placerat turpis, et consectetur mi
        efficitur eu. Cras ac consequat nibh, id hendrerit neque. || f(x) = x ||"""
        Section(name="Lorem ipsum", html_content=text_1, markdown_content=text_1, order=1, page=page_1).save()
        text_2 = """Nam eget accumsan lacus. Suspendisse molestie varius blandit. Etiam euismod leo in massa congue, id dictum neque malesuada. 
        Fusce tempor dui id urna lobortis volutpat. Morbi condimentum libero diam, at egestas neque lobortis sed. Cras rutrum porttitor feugiat. 
        Duis aliquet massa ultrices placerat aliquam. Vestibulum finibus, velit id vestibulum accumsan, ante nisl tincidunt diam, eu tempus 
        mauris justo eget justo. Fusce finibus fringilla libero, cursus mattis tellus sollicitudin sit amet. Donec commodo interdum pellentesque. 
        Ut vulputate tristique augue, id fermentum orci tempus sit amet. Suspendisse id augue magna. Praesent maximus justo eu velit ultrices 
        vehicula. Fusce tristique erat neque, quis euismod est fringilla nec. Proin sed neque non magna sollicitudin vestibulum."""
        Section(name="Pellentesque", html_content=text_2, markdown_content=text_2, order=1, page=page_1).save()
        page_2 = Page(name="Les équations", course=course, order=2)
        page_2.save()
        Section(name="Pretium", html_content=text_2, markdown_content=text_2, order=1, page=page_2).save()

        self.stdout.write('data created')