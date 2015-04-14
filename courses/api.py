from restless.modelviews import ListEndpoint, DetailEndpoint, Endpoint
from restless.models import serialize
from restless.http import Http201, Http200, HttpError

from courses.models import Course, Page, Section, CourseComment, Status, Progression, Theme
from courses.forms import CourseForm, PageForm, SectionForm, CommentForm
from courses.api_utils import *

class CourseList(ListEndpoint):
    model = Course

    # /courses
    # GET: renvoie une liste de cours
    def get(self, request):
        user = request.user
        # Trie les cours par thème, sélectionne les cours favoris d'un utilisateur ou renvoie tous les cours
        # Retourne seulement les cours publiés
        if 'theme' in request.GET:
            courses = Course.objects.filter(chapter__theme__name=request.GET['theme'], published=True)
        elif 'favorite' in request.GET and user.is_authenticated() and user.is_active:
            courses = user.favorite_courses.filter(published=True)
        else:
            courses = Course.objects.filter(published=True)
        return serialize(courses, include=[
                ('chapter', dict(fields=['name']))
            ])


    # POST: crée un nouveau cours
    @teacher_required
    def post(self, request):
        course_form = CourseForm(request.data)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.author = request.user
            course.save()
            # Crée une page vierge
            page = Page(name="Première page", order=1, course_id=course.id)
            page.save()
            # Crée une section dans la page
            page.sections.create(name="Première section", order=1)
            return Http201(self.serialize(course))

class TeacherCourseList(ListEndpoint):
    model = Course

    # /courses/all

    # GET
    @teacher_required
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    # POST: non utilisé
    def post(self, request, *args, **kwargs):
        raise HttpError(405, 'Method Not Allowed')

class CourseDetail(DetailEndpoint):
    model = Course

    # /courses/:id

    # GET
    @teacher_required
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    # PUT
    @teacher_required
    def put(self, request, *args, **kwargs):
        return super().put(self, request, *args, **kwargs)

    # DELETE: non utilisé
    def delete(self, request, *args, **kwargs):
        raise HttpError(405, 'Method Not Allowed')

class CoursePageList(ListEndpoint):
    model = Course

    # /courses/:id/pages

    # GET: non utilisé
    def get(self, request, *args, **kwargs):
        raise HttpError(405, 'Method Not Allowed')

    # POST: ajoute une page à un cours
    @teacher_required
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        # Crée une page à la suite des autres
        order = course.pages.count() + 1
        page = Page(name="Titre de la page", order=order, course_id=course.id)
        page.save()
        # Crée une section dans la nouvelle page
        page.sections.create(name="Première section", order=1)
        return Http201(serialize_page(page, course, request.user))

class PageCourseDetail(DetailEndpoint):
    model = Page

    # /pages/:id/courses/:id

    # DELETE: non utilisé
    def delete(self, request, *args, **kwargs):
        raise HttpError(405, 'Method Not Allowed')

    # GET: renvoie une page d'un cours
    def get(self, request, page_id, course_id):
        # /!\ l'argument "page_id" représente le champ "order" du modèle Page, pas l'"id"
        course = get_object_or_404(Course, id=course_id)
        try:
            page = Page.objects.get(course_id=course_id, order=page_id)
        except Page.DoesNotExist:
            page = Page(name="Page introuvable")
        return serialize_page(page, course, request.user)

    # PUT: sauvegarde le contenu d'une page
    @teacher_required
    def put(self, request, page_id, course_id):
        course = get_object_or_404(Course, id=course_id)
        # Récupère la page à éditer
        page = get_object_or_404(Page, id=page_id)
        # On utilise un formulaire (PageForm)
        # request.data est un dictionnaire contenant les données soumise par l'utilisateur
        # ici le contenu de la page
        page_form = PageForm(request.data, instance=page)
        # On vérifie si les informations sont présentes et valides
        if page_form.is_valid():
            # On enregistre la page - sauvegarde le titre
            page_form.save()
        # On récupère le dictionnaire contenant les données des sections
        sections_params = request.data['sections']
        # On fait une boucle pour chaque section
        for section_params in sections_params:
            # On récupère la section
            section = Section.objects.get(id=section_params['id'])
            # On utilise un formulaire (SectionForm)
            # section_params est un dictionnaire contenant le titre et le contenu de la section
            section_form = SectionForm(section_params, instance=section)
            # On vérifie si les informations sont présentes et valides
            if section_form.is_valid():
                # On enregistre la section
                section_form.save()
        return Http200(serialize_page(page, course, request.user))

class PageSectionList(ListEndpoint):
    model = Section

    # /pages/:id/sections

    # GET: non utilisé
    def get(self, request, *args, **kwargs):
        raise HttpError(405, 'Method Not Allowed')
    
    # POST: Crée une nouvelle section dans une page
    @teacher_required
    def post(self, request, page_id):
        page = get_object_or_404(Page, id=page_id)
        # Crée une section à la suite des autres
        order = page.sections.count() + 1
        section = page.sections.create(name="Editer ici", markdown_content="Et ici", order=order)
        section.save()
        return Http201(serialize_page(page, page.course, request.user))

class SectionDetail(DetailEndpoint):
    model = Section

    # /sections/:id

    # GET: non utilisé
    def get(self, request, *args, **kwargs):
        raise HttpError(405, 'Method Not Allowed')

    # PUT: non utilisé
    def put(self, request, *args, **kwargs):
        raise HttpError(405, 'Method Not Allowed')

    # DELETE
    @teacher_required
    def delete(self, request, *args, **kwargs):
        return super().delete(self, request, *args, **kwargs)


class ThemeList(ListEndpoint):
    model = Theme

    # /themes
    # POST

    # GET: renvoie tous les thèmes et leurs chapitres
    def get(self, request):
        themes = Theme.objects.all()
        return serialize(themes, include=[
                ('chapters', dict())
            ])

class CommentList(ListEndpoint):
    model = CourseComment

    # courses/:id/comments
    # GET: renvoie les commentaires d'un cours
    def get(self, request, pk):
        comments = CourseComment.objects.filter(course_id=pk)
        return serialize(comments, include=[
                ('user', lambda c: c.user.username)
            ])


    # POST: crée un commentaire dans un cours
    @login_required
    def post(self, request, pk):
        comment_form = CommentForm(request.data)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.course_id = pk
            comment.save()
            return Http201(serialize(comment, include=[
                ('user', lambda c: c.user.username)
            ]))

class CourseMenu(Endpoint):

    # Renvoie le titre des pages et de leurs sections pour faire le menu du cours
    def get(self, request, pk):
        pages = Page.objects.filter(course_id=pk)
        # on inclut le champs "order" pour mettre en évidence la page active dans le menu
        return serialize(pages, fields=[
                'name',
                'order',
                ('sections', dict(fields=['name']))
            ])

class CoursePageProgress(Endpoint):

    # Marque la progression d'un utilisateur
    @login_required
    def put(self, request, pk):
        user = request.user
        # On récupère la page concernée
        page = get_object_or_404(Page, id=pk)

        # request.data est un dictionnaire contenant les données soumises par l'utilisateur
        # ici, si l'utilisateur a compris ou non la page
        # On choisit le statut en fonction
        if request.data['is_done'] == True:
            status = Status.objects.get(name="Compris")
        else:
            status = Status.objects.get(name="Relire")

        # Si l'utilisateur n'a pas encore marqué sa progression sur cette page
        if not page.state(user):
            # On crée une progression avec la page, le statut et l'utilisateur
            page.progression_set.create(status=status, user=user)
        # si l'utilisateur a déjà marqué sa progression sur cette page
        else:
            # On récupère sa progression
            progression = page.progression_set.get(user=user)
            # On met à jour avec le nouveau statut
            progression.status = status
            progression.save()
        return Http200({"progression": status.name, "percentage": page.course.percentage()})

class CoursePublish(Endpoint):

    # Publie ou retire un cours
    @teacher_required
    def put(self, request, pk):
        course = get_object_or_404(Course, id=pk)
        # on inverse le booléen "published" qui détermine si le cours est publié ou non
        course.published = not course.published
        course.save()
        return Http200({"published": course.published})

class CourseFavorite(Endpoint):

    # Ajoute ou retire un cours des favoris de l'utilisateur
    @login_required
    def post(self, request, pk):
        user = request.user
        course = get_object_or_404(Course, id=pk)
        # teste si l'utilisateur a déjà le cours dans ses favoris
        is_favorite = course.has_favorite(user)
        if is_favorite:
            # on retire le cours des favoris
            course.favorites.remove(user)
        else:
            # on ajoute le cours aux favoris
            course.favorites.add(user)
        return Http201({"favorite": not is_favorite})
