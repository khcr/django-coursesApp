from restless.models import serialize
# TODO: use the current user
from django.contrib.auth.models import User

# api.py: return a valid page JSON object included course and sections
def serialize_page(page, course):
    # TODO: use the current user
    user = User.objects.first()
    return serialize(page, include=[
        (
            'course', lambda a: {
                'id': course.id,
                'name': course.name, 
                'description': course.description,
                'percentage': course.percentage(),
                'published': course.published,
                'favorite': course.has_favorite(user),
            }
        ),
            ('sections', dict()),
            ('total_pages', lambda a: course.total_pages()),
            ('progression', lambda a: a.state(user)),
        ])

def clear_tables(models):
    for model in models:
        model.objects.all().delete()