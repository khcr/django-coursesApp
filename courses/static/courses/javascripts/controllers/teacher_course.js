"use strict";

var app = angular.module("controllers");

app.controller("TeacherCourseController", ["$scope", "Course", function($scope, Course) {  
  
  // récupère tous les cours, publiés ou non
  $scope.courses = Course.query({resource: "all"});

}]);