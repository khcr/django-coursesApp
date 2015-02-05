var app = angular.module('controllers');

app.controller('HomeCourseController', ['$scope', '$location', 'Course', function($scope, $location, Course) {
  $scope.courses = Course.query();

  $scope.showCourse = function(course) {
    $location.path(course.id + "/view/1");
  };

}]);