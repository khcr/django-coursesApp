"use strict";

var app = angular.module("routes");

app.config(function($routeProvider, $resourceProvider){
  var basePath = "/static/courses/html/";
  $routeProvider.when("/", {
      templateUrl: basePath + "home.html",
      controller: "HomeCourseController"
    })
    .when("/about", {
      templateUrl: basePath + "about.html",
      controller: "AboutController"
    })
    .when("/new", {
      templateUrl: basePath + "new.html",
      controller: "NewCourseController"
    })
    .when("/:courseId/view/:pageId", {
      templateUrl: basePath + "show.html",
      controller: "ShowCourseController"
    })
    .when("/:courseId/edit/:pageId", {
      templateUrl: basePath + "page_edit.html",
      controller: "EditPageController"
    })
    .when("/:courseId/edit", {
      templateUrl: basePath + "edit.html",
      controller: "EditCourseController"
    })
    .when("/:courseId/preview/:pageId", {
      templateUrl: basePath + "preview.html",
      controller: "PreviewCourseController"
    })
    .when("/help", {
      templateUrl: basePath + "help.html"
    })
    .when("/teacher/courses", {
      templateUrl: basePath + "teacher_course.html",
      controller: "TeacherCourseController"
    })
    .otherwise({
      templateUrl: basePath + "404.html"
    });
    $resourceProvider.defaults.stripTrailingSlashes = true;
});