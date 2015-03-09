from django.conf.urls import patterns, url, include

from courses import views
from courses.api import CourseList, TeacherCourseList, CourseDetail, PageCourseDetail, PageSectionList, CoursePageList, SectionDetail, ThemeList, CommentList, CourseMenu, CoursePageProgress, CoursePublish, CourseFavorite

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^api/courses$', CourseList.as_view()),
    url(r'^api/courses/all$', TeacherCourseList.as_view()),
    url(r'^api/courses/(?P<pk>\d+)$', CourseDetail.as_view()),
    url(r'^api/pages/(?P<page_id>\d+)/courses/(?P<course_id>\d+)$', PageCourseDetail.as_view()),
    url(r'^api/themes$', ThemeList.as_view()),
    url(r'^api/pages/(?P<page_id>\d+)/sections$', PageSectionList.as_view()),
    url(r'^api/courses/(?P<course_id>\d+)/pages$', CoursePageList.as_view()),
    url(r'^api/sections/(?P<pk>\d+)$', SectionDetail.as_view()),
    url(r'^api/courses/(?P<pk>\d+)/comments$', CommentList.as_view()),
    url(r'^api/courses/(?P<pk>\d+)/menu$', CourseMenu.as_view()),
    url(r'^api/courses/(?P<pk>\d+)/publish$', CoursePublish.as_view()),
    url(r'^api/courses/(?P<pk>\d+)/favorite$', CourseFavorite.as_view()),
    url(r'^api/pages/(?P<pk>\d+)/progression$', CoursePageProgress.as_view()),
    url(r"^pdf/(?P<pk>\d+)/.*\.pdf$", views.pdf, name="pdf")
)