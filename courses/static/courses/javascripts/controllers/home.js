"use strict";

var app = angular.module("controllers");

app.controller("HomeCourseController", ["$scope", "$location", "$http", "Course", function($scope, $location, $http, Course) {

  // récupère tous les cours
  $scope.courses = Course.query();

  // pour générer les boutons afin de trier les cours
  $http.get("api/themes").success(function(themes) {
    $scope.themes = themes;
  });

  // pour distinguer l'onglet sélectionné
  // triage par défaut des cours = "Tous"
  var current = "Tous";

  // trie les cours en affichant les favoris de l'utilisateur
  $scope.selectFavorites = function() {
    current = "Favoris";
    $scope.courses = Course.query({favorite: "true"});
  };

  // trie les cours par thème
  $scope.changeCategory = function(theme) {
    current = theme || "Tous";
    $scope.courses = Course.query({theme: theme});
  };

  // teste si une catégorie est l'onglet sélectionné
  $scope.currentCategory = function(category) {
    return category === current;
  };

  // redirige vers la lecture d'un cours
  $scope.showCourse = function(course) {
    $location.path(course.id + "/view/1");
  };

}]);