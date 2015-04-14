"use strict";

var app = angular.module("controllers");

app.controller("ShowCourseController", ["$scope", "$routeParams", "$location", "Page", "Comment", "$http", function($scope, $routeParams, $location, Page, Comment, $http) {
  
  // récupère la page et son contenu
  $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
    $scope.course = page.course;

    // pour désactiver les liens de changement de page
    // teste si la page actuelle est la première page
    $scope.firstPage = function() {
      return $scope.page.order === 1;
    };

    // teste si la page actuelle est la dernière page
    $scope.lastPage = function() {
      return $scope.page.order === $scope.page.total_pages;
    };

  });

  // redirige vers la prochaine page du cours
  $scope.nextPage = function() {
    $location.path($scope.course.id + "/view/" + ($scope.page.order + 1));
  };

  // redirige vers la précédente page du cours
  $scope.previousPage = function() {
    $location.path($scope.course.id + "/view/" + ($scope.page.order - 1));
  };

  // pour générer le menu du cours
  $http.get("api/courses/" + $routeParams.courseId + "/menu").success(function(pages) {
    $scope.pages = pages;
  });

  // teste si une page est la page actuelle
  $scope.isCurrentPage = function(page) {
    return page.order === $scope.page.order;
  };

  // teste si l'utilisateur a marqué une certaine progression sur la page
  // pour changer les liens en conséquence
  $scope.isProgress = function(name) {
    return $scope.page.progression === name;
  };

  // sauvegarde une progression de la page
  $scope.saveProgress = function(isDone) {
    // sauvegarde la progression dans la base de données
    $http.put("api/pages/" + $scope.page.id + "/progression", {is_done: isDone}).
      success(function(response) {
        // redirige vers la page suivante, si ce n'est pas la dernière page
        if( !$scope.lastPage() ) {
          $scope.nextPage();
        // sinon, met à jour les boutons et la barre de progression en fonction de la nouvelle progression
        } else {
          $scope.page.progression = response.progression;
          $scope.page.course.percentage = response.percentage;
        }
      });
  };

  // ajoute/retire un cours des favoris
  $scope.favorite = function() {
    $http.post("api/courses/" + $routeParams.courseId + "/favorite").success(function(response) {
      $scope.course.favorite = response.favorite;
    });
  };
  
  // affiche un message d'attente sur la page pendant que le PDF est généré
  $scope.wait = function() {
    $scope.wait = "Merci de patienter..."
  };

  /* Commentaires */

  // récupère tous les commentaires du cours
  $scope.comments = Comment.query({courseId: $routeParams.courseId});

  // par défaut, les commentaires sont masqués
  $scope.showComments = false;

  // affiche/cache la section des commentaires
  $scope.toggleComments = function() {
    $scope.showComments = !$scope.showComments;
  };

  // crée un commentaire d'exemple, affiché dans le formulaire pour ajouter un commentaire
  var newComment = new Comment({"placeholder":"Ton commentaire", course_id: $routeParams.courseId});
  // Object.create permet de cloner une variable
  $scope.comment = Object.create(newComment);

  // ajoute un commentaire au cours
  $scope.saveComment = function() {
    // ajoute le commentaire dans la base de données
    $scope.comment.$save(function(comment) {
      // ajoute le nouveau commentaire à la page
      $scope.comments.push(comment);
      // remet un commentaire d'exemple dans le formulaire
      $scope.comment = Object.create(newComment);
    });
  };

}]);