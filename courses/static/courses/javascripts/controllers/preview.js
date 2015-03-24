"use strict";

var app = angular.module("controllers");

app.controller("PreviewCourseController", ["$scope", "$routeParams", "Page", function($scope, $routeParams, Page) {

  // récupère la page et son contenu
  $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
    $scope.course = page.course;
  });
  
}]);