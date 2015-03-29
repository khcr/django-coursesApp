"use strict";

var app = angular.module("controllers");

app.controller("EditPageController", ["$scope", "$routeParams", "$location", "Section", "$filter", "Page", "Course", "$interval", "$http",
  function($scope, $routeParams, $location, Section, $filter, Page, Course, $interval, $http) {

    // récupère la page et son contenu
    $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
      $scope.course = new Course(page.course);
    });

    // ajoute une section à la page
    $scope.newSection = function() {
      $scope.saveCourse();
      $scope.page.$add_section();
    };

    // supprime une section de la page
    $scope.removeSection = function(key) {
      // réorganise l'ordre des sections se trouvant après celle supprimée
      for(var i = key + 1; i < $scope.page.sections.length; i++) {
        // étant donné qu'une section a été supprimée, il faut reculer l'ordre des sections suivantes de 1
        $scope.page.sections[i].order -= 1;
      }
      var section = new Section($scope.page.sections[key]);
      // fait une requête pour supprimer la section de la base de données
      section.$delete(function() {
        // retire la section de notre objet contenant toutes les sections
        $scope.page.sections.splice(key, 1);
        // sauvegarde la page
        $scope.saveCourse();
      });
    };

    // monte une section dans la page
    $scope.upSection = function(key) {
      // vérifie que la section n'est pas tout en haut
      if(key !== 0) {
        // inverse deux sections
        $scope.page.sections[key].order -= 1;
        $scope.page.sections[key - 1].order += 1;
        // sauvegarde la page
        $scope.saveCourse();
      }
    };

    // descend une section dans la page
    $scope.downSection = function(key) {
      // vérifie que la section n'est pas tout en bas
      if($scope.page.sections[key + 1] !== undefined) {
        // inverse deux sections
        $scope.page.sections[key].order += 1;
        $scope.page.sections[key + 1].order -= 1;
        // sauvegarde la page
        $scope.saveCourse();
      }
    };

    // sauvegarde la page
    $scope.saveCourse = function() {
      // convertit le contenu de Markdown à HTML
      angular.forEach($scope.page.sections, function(value, key) {
        var section = $scope.page.sections[key];
        // teste si la section n'est pas vide
        if(section.markdown_content !== undefined) {
          section.html_content = $filter("markdown")(section.markdown_content);
        }
      });
      // sauvegarde la page dans la base de données
      $scope.page.$update({ objectId: $scope.course.id }, function() {
        // change la date de la dernière sauvegarde, affichée sur la page
        $scope.lastSave = new Date();
      });
    };

    // sauvegarde la page toutes les 30 secondes
    var interval = $interval($scope.saveCourse, 30000);
    $scope.lastSave = new Date();

    // sauvegarde la page quand l'utilisateur quitte la page
    $scope.$on("$destroy", function(){
      // stop la sauvegarde automatique
      $interval.cancel(interval);
      // sauvegarde la page
      $scope.saveCourse();
    });

    // ajoute une nouvelle page au cours
    $scope.newPage = function() {
      // sauvegarde la page
      $scope.saveCourse();
      // ajoute une page dans la base de données
      $scope.course.$add_page(function(page) {
        $scope.page = page;
        $scope.course = page.course;
        // redirige vers l'édition de la nouvelle page
        $location.path($scope.course.id + "/edit/" + $scope.page.order);
      });
      
    };

    // teste si une page est la page actuelle
    $scope.isCurrentPage = function(number) {
      return number == $routeParams.pageId;
    };

    // prévisualise un cours
    $scope.preview = function() {
      // sauvegarde la page
      $scope.saveCourse();
      // redirige vers la page de prévisualisation
      $location.path($scope.course.id + "/preview/" + $scope.page.order);
    };

    // publie ou retire un cours
    $scope.publish = function() {
      // sauvegarde la page
      $scope.saveCourse();
      // publie ou retire le cours dans la base de données
      $http.put("api/courses/" + $routeParams.courseId + "/publish").success(function(response) {
        // met à jour l'état du cours, affiché sur la page
        $scope.course.published = response.published;
      });
    };

  }
]);