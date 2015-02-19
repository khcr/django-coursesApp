from restless.modelviews import ListEndpoint, DetailEndpoint, Endpoint
from restless.models import serialize
from restless.http import Http201, Http200

from courses.models import Course, Page, Section, CourseComment, Status, Progression
from courses.forms import CourseForm, PageForm, SectionForm, CommentForm
from courses.utils import serialize_page
from teachers.models import Theme, Teacher
from django.contrib.auth.models import User

class CourseList(ListEndpoint):
    model = Course

    # /courses
    # GET
    def get(self, request):
        # TODO: use the current user
        user = User.objects.first()
        if 'theme' in request.GET:
            courses = Course.objects.filter(chapter__theme__name=request.GET['theme'])
        elif 'favorite' in request.GET:
            courses = user.favorite_courses.all()
        else:
            courses = Course.objects.all()
        return serialize(courses)


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

    # /pages/id/courses/id
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
    model = Theme

    # /themes
    # POST

    # GET: get all themes included the chapters
    def get(self, request):
        themes = Theme.objects.all()
        return serialize(themes, include=[
                ('chapters', dict())
            ])

class CommentList(ListEndpoint):
    model = CourseComment

    # /comments
    # GET
    def get(self, request, pk):
        comments = CourseComment.objects.filter(course_id=pk)
        return serialize(comments, include=[
                ('user', lambda c: c.user.username)
            ])


    # POST: get all comments for a course
    def post(self, request, pk):
        comment_form = CommentForm(request.data)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            # TODO: use the current user
            comment.user = User.objects.first()
            comment.course_id = pk
            comment.save()
            return Http201(serialize(comment, include=[
                ('user', lambda c: c.user.username)
            ]))

class CourseMenu(Endpoint):

    def get(self, request, pk):
        pages = Page.objects.filter(course_id=pk)
        return serialize(pages, fields=[
                'name',
                'order',
                ('sections', dict(fields=['name']))
            ])

class CoursePageProgress(Endpoint):

    def put(self, request, pk):
        # TODO: use the current user
        user = User.objects.first()
        page = Page.objects.get(id=pk)
        if request.data['is_done'] == True:
            status = Status.objects.get(name="Compris")
        else:
            status = Status.objects.get(name="Relire")
        if not page.state(user):
            page.progression_set.create(status=status, user=user)
        else:
            progression = page.progression_set.get(user=user)
            progression.status = status
            progression.save()
        return Http200({"progression": status.name, "percentage": page.course.percentage()})

class CoursePublish(Endpoint):

    def put(self, request, pk):
        course = Course.objects.get(id=pk)
        course.published = not course.published
        course.save()
        return Http200({"published": course.published})

class CourseFavorite(Endpoint):

    def post(self, request, pk):
        # TODO: use the current user
        user = User.objects.first()
        course = Course.objects.get(pk=pk)
        is_favorite = course.has_favorite(user)
        if is_favorite:
            course.favorites.remove(user)
        else:
            course.favorites.add(user)
        return Http201({"favorite": not is_favorite})
