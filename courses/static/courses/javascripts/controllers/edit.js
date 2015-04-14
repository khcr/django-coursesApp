"use strict";

var app = angular.module("controllers");

app.controller("EditCourseController", ["$scope", "$routeParams", "$http", "Course", function($scope, $routeParams, $http, Course) {

  // récupère le cours
  $scope.course = Course.get({courseId: $routeParams.courseId});

  // pour le lien de retour au cours
  $scope.page = {order: 1};

  // pour générer la sélection de catégories
  $http.get("api/themes").success(function(themes) {
    $scope.themes = themes;
  });

  $scope.saveCourse = function() {
    $scope.course.$update(function() {
      // message affiché sur la page
      $scope.message = "Sauvegardé";
    });
  };

}]);