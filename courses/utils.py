from restless.models import serialize
# TODO: utiliser l'utilisateur connecté
from django.contrib.auth.models import User

# retourne un objet JSON contenant les informations du cours, la page du cours et ses sections, le nombre total de page et la progression
# serialize est une méthode RestLess
def serialize_page(page, course):
    # TODO: utiliser l'utilisateur connecté
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

# efface les enregistrements de plusieurs tables
# prend un tableau en argument
def clear_tables(models):
    for model in models:
        model.objects.all().delete()