"use strict";

var app = angular.module("controllers");

app.controller("HomeCourseController", ["$scope", "$location", "$http", "Course", function($scope, $location, $http, Course) {

  $scope.courses = Course.query();

  $http.get("api/themes").success(function(themes) {
    $scope.themes = themes;
  });

  var current = "Tous";

  $scope.selectFavorites = function() {
    current = "Favoris";
    $scope.courses = Course.query({favorite: "true"});
  };

  $scope.changeCategory = function(theme) {
    current = theme || "Tous";
    $scope.courses = Course.query({theme: theme});
  };

  $scope.currentCategory = function(category) {
    return category === current;
  };

  $scope.showCourse = function(course) {
    $location.path(course.id + "/view/1");
  };

}]);