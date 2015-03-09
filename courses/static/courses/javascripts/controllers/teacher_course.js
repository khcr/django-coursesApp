"use strict";

var app = angular.module("controllers");

app.controller("TeacherCourseController", ["$scope", "Course", function($scope, Course) {  
  
  $scope.courses = Course.query({resource: "all"});

}]);