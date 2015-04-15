"use strict";

var app = angular.module("routes");

// routes de l'application
app.config(function($routeProvider, $resourceProvider){
  var basePath = "/static/courses/html/",
      teacherPath = "/courses/teacher/templates/",
      userPath = "/courses/user/templates/";

  $routeProvider.when("/", {
      templateUrl: userPath + "home.html",
      controller: "HomeCourseController"
    })
    .when("/about", {
      templateUrl: basePath + "about.html"
    })
    .when("/new", {
      templateUrl: teacherPath + "new.html",
      controller: "NewCourseController"
    })
    .when("/:courseId/view/:pageId", {
      templateUrl: userPath + "show.html",
      controller: "ShowCourseController"
    })
    .when("/:courseId/edit/:pageId", {
      templateUrl: teacherPath + "page_edit.html",
      controller: "EditPageController"
    })
    .when("/:courseId/edit", {
      templateUrl: teacherPath + "edit.html",
      controller: "EditCourseController"
    })
    .when("/:courseId/preview/:pageId", {
      templateUrl: teacherPath + "preview.html",
      controller: "PreviewCourseController"
    })
    .when("/help", {
      templateUrl: teacherPath + "help.html"
    })
    .when("/teacher/courses", {
      templateUrl: teacherPath + "teacher_course.html",
      controller: "TeacherCourseController"
    })
    .otherwise({ // Page 404
      templateUrl: basePath + "404.html"
    });
    $resourceProvider.defaults.stripTrailingSlashes = true;
});