from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
import re

from tempfile import NamedTemporaryFile
import subprocess

from courses.models import Course

def index(request):
    return render(request, "courses/courses.html", locals())

def pdf(request, pk):
    response = HttpResponse(content_type='application/pdf')

    course = get_object_or_404(Course, pk=pk)
    template = get_template("courses/pdf.md")
    content = template.render(RequestContext(request, {"course": course}))
    content = re.sub(r"\|{2}(?P<content>[^|]*)\|{2}", r"\\begin{math}\g<content>\end{math}", content)

    output_file = NamedTemporaryFile(suffix='.pdf')
    p = subprocess.Popen(['pandoc', '--from=markdown', '--to=latex', '-o', output_file.name, '--latex-engine=xelatex', '-s', "-V" ,"geometry:margin=1in"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    c = p.communicate(content.encode('utf-8'))[0].decode('utf-8')

    response.write(output_file.read())
    return response