"use strict";

var app = angular.module("controllers");

app.controller("EditCourseController", ["$scope", "$routeParams", "$http","Course", function($scope, $routeParams, $http, Course) {

  $scope.course = Course.get({courseId: $routeParams.courseId, resources: ""});
  $scope.page = {order: 1};

  $http.get("api/themes").success(function(themes) {
    $scope.themes = themes;
  });

  $scope.saveCourse = function() {
    $scope.course.$update(function() {
      $scope.message = "Sauvegardé";
    });
  };

}]);