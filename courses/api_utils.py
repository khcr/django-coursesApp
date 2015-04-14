from restless.models import serialize
from restless.http import HttpError, Http403

# retourne un objet JSON contenant les informations du cours, la page du cours et ses sections, le nombre total de page et la progression
# serialize est une méthode RestLess
def serialize_page(page, course, user):
    course_params = {
        'id': course.id,
        'name': course.name, 
        'description': course.description,
        'published': course.published,
    }
    is_user = user.is_authenticated() and user.is_active
    if is_user:
        course_params['percentage'] = course.percentage()
        course_params['favorite'] = course.has_favorite(user)

    return serialize(page, include=[
        (
            'course', lambda a: course_params
        ),
            ('sections', dict()),
            ('total_pages', lambda a: course.total_pages()),
            ('progression', lambda a: a.state(user) if is_user else None)
        ])


# retourne un enregistrement ou sinon une erreur 404
# inspiré de:
# https://github.com/django/django/blob/a52cd407b86a51e1badf6771e590361e24fd7155/django/shortcuts.py
def get_object_or_404(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        raise HttpError(404, 'Resource Not Found')


# décorateur qui autorise l'accès aux enseigants seulement
# inspiré de:
# https://django-restless.readthedocs.org/en/latest/_modules/restless/auth.html#login_required
def teacher_required(fn):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.user.is_teacher():
            return Http403('forbidden')
        return fn(self, request, *args, **kwargs)
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper

# décorateur qui autorise l'accès aux utilisateurs connectés seulement
def login_required(fn):
    def wrapper(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.user.is_active:
            return Http403('forbidden')
        return fn(self, request, *args, **kwargs)
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper