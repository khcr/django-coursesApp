from restless.modelviews import ListEndpoint, DetailEndpoint
from restless.models import serialize
from restless.http import Http201, Http200

from courses.models import Course, Page, Section
from courses.forms import CourseForm, PageForm, SectionForm
from courses.utils import serialize_page
from teachers.models import Theme, Teacher

class CourseList(ListEndpoint):
    model = Course

    # /courses
    # GET

    # POST: create a new course
    def post(self, request):
        course_form = CourseForm(request.data)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.author = Teacher.objects.first()
            course.save()
            page = Page(name="Première page", order=1, course_id=course.id)
            page.save()
            page.sections.create(name="Première section", order=1)
            return Http201(self.serialize(course))


class CourseDetail(DetailEndpoint):
    model = Course

    # /courses/id
    # GET
    # PUT
    # DELETE

class CoursePageList(ListEndpoint):
    model = Course

    # /courses/id/pages
    # GET

    # POST: add a new page to a course
    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        order = course.pages.count() + 1
        page = Page(name="Titre de la page", order=order, course_id=course.id)
        page.save()
        page.sections.create(name="Première section", order=1)
        return Http201(serialize_page(page, course))

class PageCourseDetail(DetailEndpoint):
    model = Page

    # /courses/id/pages/id
    # DELETE

    # GET: get all pages for a course
    def get(self, request, page_id, course_id):
        course = Course.objects.get(id=course_id)
        page = course.pages.get(order=page_id)
        return serialize_page(page, course)

    # PUT: save the page's content
    def put(self, request, page_id, course_id):
        course = Course.objects.get(id=course_id)
        page = Page.objects.get(id=page_id)
        page_form = PageForm(request.data, instance=page)
        if page_form.is_valid():
            page_form.save()
        sections_params = request.data['sections']
        for section_params in sections_params:
            section = Section.objects.get(id=section_params['id'])
            section_form = SectionForm(section_params, instance=section)
            if section_form.is_valid():
                section_form.save()
        return Http200(serialize_page(page, course))

class PageSectionList(ListEndpoint):
    model = Section

    # /pages/id/sections
    # GET
    
    # POST: Add a new section to a page
    def post(self, request, page_id):
        page = Page.objects.get(id=page_id)
        order = page.sections.count() + 1
        section = page.sections.create(name="Editer ici", markdown_content="Et ici", order=order)
        section.save()
        return Http201(serialize_page(page, page.course))

class SectionDetail(DetailEndpoint):
    model = Section

    # /section/id
    # GET
    # PUT
    # DELETE


class ThemeList(ListEndpoint):

    # /themes
    # POST

    # GET: get all themes included the chapters
    def get(self, request):
        themes = Theme.objects.all()
        return serialize(themes, include=[
                ('chapters', dict())
            ])