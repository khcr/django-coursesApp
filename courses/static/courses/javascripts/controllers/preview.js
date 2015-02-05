var app = angular.module('controllers');

app.controller('PreviewCourseController', ['$scope', '$routeParams', 'Page', function($scope, $routeParams, Page) {
  $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
    $scope.course = page.course
  })
}]);