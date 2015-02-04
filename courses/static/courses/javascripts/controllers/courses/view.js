var app = angular.module('controllers');

app.controller('ViewCourseController', ['$scope', '$routeParams', '$location', 'Page', function($scope, $routeParams, $location, Page) {
  $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
    $scope.course = page.course
    
    $scope.firstPage = function() {
      return $scope.page.order === 1;
    };
    $scope.lastPage = function() {
      return $scope.page.order === $scope.page.total_pages;
    };

  });

  $scope.nextPage = function() {
    $location.path($scope.course.id + "/view/" + ($scope.page.order + 1));
  };
  $scope.previousPage = function() {
    $location.path($scope.course.id + "/view/" + ($scope.page.order - 1));
  };
}]);