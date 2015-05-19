"use strict";

// https://docs.angularjs.org/api/ngResource/service/$resource

var app = angular.module("resources");

app.factory("Course", ["$resource", function($resource) {
  return $resource(
    "api/courses/:courseId/:resource",
    {courseId: "@id"},
    {
      update: { method: "PUT" }
    }
  );
}]);

app.factory("Page", ["$resource", function($resource) {
  return $resource(
    "api/pages/:pageId/:resource/:objectId",
    {pageId: "@id", resource: "courses"},
    {
      update: { method: "PUT" },
      // ajoute une section à la page
      add_section: { method: "POST", params: {resource: "sections" }},
      // ajoute une page au cours
      add_page: { method: "POST", params: { pageId: null, resource: null }, url: "api/courses/:courseId/pages" }
    }
  );
}]);

app.factory("Section", ["$resource", function($resource) {
  return $resource(
    "api/sections/:sectionId",
    {sectionId: "@id"}
  );
}]);

app.factory("Comment", ["$resource", function($resource) {
  return $resource(
    "api/courses/:courseId/comments/:commentId",
    {courseId: "@course_id", commentId: "@id"}
  );
}]);