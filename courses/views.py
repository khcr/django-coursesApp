from django.shortcuts import render
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from weasyprint import HTML
import re

from courses.models import Course

def index(request):
    return render(request, "courses/courses.html", locals())

def pdf(request, pk):
    # https://www.ampad.de/blog/generating-pdfs-django/
    course = Course.objects.get(id=pk)
    template = get_template("courses/pdf.html")
    context = {"course": course}
    html = template.render(RequestContext(request, context))
    html = re.sub(r"\|{2}(?P<content>[^|]*)\|{2}", "<div class='math'>\g<content></div>", html)
    response = HttpResponse(content_type="application/pdf")
    HTML(string=html).write_pdf(response)
    return response