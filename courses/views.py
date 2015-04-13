from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.template import RequestContext, TemplateDoesNotExist
from django.http import HttpResponse
import re

from tempfile import NamedTemporaryFile
import subprocess

from courses.models import Course

# point de départ du site, AngularJS s'occupe du reste des URL
# courses.html est le layout de l'application
def index(request):
    return render(request, "courses/courses.html", locals())

# retourne les gabarits HTML pour AngularJS, accessible seulement pour les enseignants
def teacher_templates(request, filename):
    if request.user.is_authenticated() and request.user.is_teacher():
        return render(request, "courses/teacher/{}".format(filename))
    else:
        return render(request, "courses/unauthorized.html")

# retourne les gabarits HTML pour AngularJS en modifiant le contenu si un utilisateur est connecté
def user_templates(request, filename):
    return render(request, "courses/user/{}".format(filename))

# retourne un cours au format PDF
def pdf(request, pk):
    # réponse HTTP en PDF
    response = HttpResponse(content_type='application/pdf')

    # récupère le cours
    course = get_object_or_404(Course, pk=pk)
    # récupère le template PDF
    template = get_template("courses/pdf.md")
    # Compile le template avec les informations du cours
    content = template.render(RequestContext(request, {"course": course}))
    # Formate les mathématiques
    # REGEX: on remplace les balises "||" du cours avec l'expression LaTex \begin{math}\end{math}. Besoin de Pandoc.
    content = re.sub(r"\|{2}(?P<content>[^|]*)\|{2}", r"\\begin{math}\g<content>\end{math}", content)

    # Inspiré de Pypandoc: https://github.com/bebraw/pypandoc
    # Rendu PDF avec Pandoc
    # On utilise un fichier temporaire pour écrire le PDF
    output_file = NamedTemporaryFile(suffix='.pdf')
    p = subprocess.Popen(['pandoc', '--from=markdown', '--to=latex', '-o', output_file.name, 
        '--latex-engine=xelatex', '-s', "-V" ,"geometry:margin=1in"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    c = p.communicate(content.encode('utf-8'))[0].decode('utf-8')

    # ajoute le PDF à notre objet réponse
    response.write(output_file.read())
    # retourne la réponse, le PDF du cours
    return response