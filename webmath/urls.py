from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns('',
    # redirige la racine du site à l'URL /courses
    url(r'^$', RedirectView.as_view(url='/courses/')),
    # site d'administration Djanfo
    url(r'^admin/', include(admin.site.urls)),
    # Login (vue générique Django)
    url(r'^login/', 'django.contrib.auth.views.login'),
    # Logout (vue générique Django)
    url(r'^logout/', 'django.contrib.auth.views.logout', {"next_page": "/courses/#"}),
    # Inclue les URL de l'application courses
    url(r'^courses/', include('courses.urls')),
)
