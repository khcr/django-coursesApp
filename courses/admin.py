from django.contrib import admin
from courses.models import Course, Page, Section, Status

admin.site.register(Course)
admin.site.register(Page)
admin.site.register(Section)
admin.site.register(Status)
