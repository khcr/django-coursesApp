"use strict";

var app = angular.module("controllers");

app.controller("NewCourseController", ["$scope", "$location", "$http", "Course", function($scope, $location, $http, Course) {
  $http.get("api/themes").success(function(themes) {
    $scope.themes = themes;
  });

  $scope.saveCourse = function() {
    var course = new Course($scope.course);
    course.$save(function(course) {
      $location.path(course.id + "/edit/1");
    });
  };
}]);