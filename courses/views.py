from django.shortcuts import render, get_object_or_404
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
    course = get_object_or_404(Course, pk=pk)
    template = get_template("courses/pdf.html")
    html = template.render(RequestContext(request, {"course": course}))
    # replace maths expressions
    html = re.sub(r"\|{2}(?P<content>[^|]*)\|{2}", "<div class='math'><img src='http://latex.codecogs.com/gif.latex?\g<content>'></div>", html)
    response = HttpResponse(content_type="application/pdf")
    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response