"use strict";

var app = angular.module("controllers");

app.controller("EditPageController", ["$scope", "$routeParams", "$location", "$upload", "Section", "$filter", "Page", "Course", "$interval", "$http",
  function($scope, $routeParams, $location, $upload, Section, $filter, Page, Course, $interval, $http) {

    $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
      $scope.course = new Course(page.course);
    });

    $scope.newSection = function() {
      $scope.saveCourse();
      $scope.page.$add_section();
    };
    $scope.removeSection = function(key) {
      for(var i = key + 1; i < $scope.page.sections.length; i++) {
        $scope.page.sections[i].order -= 1;
      }
      var section = new Section($scope.page.sections[key]);
      section.$delete(function() {
        $scope.page.sections.splice(key, 1);
        $scope.saveCourse();
      });
    };
    $scope.upSection = function(key) {
      if(key !== 0) {
        $scope.page.sections[key].order -= 1;
        $scope.page.sections[key - 1].order += 1;
        $scope.saveCourse();
      }
    };
    $scope.downSection = function(key) {
      if($scope.page.sections[key + 1] !== undefined) {
        $scope.page.sections[key].order += 1;
        $scope.page.sections[key + 1].order -= 1;
        $scope.saveCourse();
      }
    };
    $scope.saveCourse = function() {
      angular.forEach($scope.page.sections, function(value, key) {
        $scope.page.sections[key].html_content = $filter("markdown")($scope.page.sections[key].markdown_content);
      });
      $scope.page.$update({ objectId: $scope.course.id }, function() {
        $scope.lastSave = new Date();
      });
    };

    var interval = $interval($scope.saveCourse, 30000);
    $scope.lastSave = new Date();

    $scope.$on("$destroy", function(){
      $interval.cancel(interval);
      $scope.saveCourse();
    });

    $scope.newPage = function() {
      $scope.saveCourse();
      $scope.course.$add_page(function(page) {
        $scope.page = page;
        $scope.course = page.course;
        $location.path($scope.course.id + "/edit/" + $scope.page.order);
      });
      
    };
    $scope.isCurrentPage = function(number) {
      return number == $routeParams.pageId;
    };
    $scope.preview = function() {
      $scope.saveCourse();
      $location.path($scope.course.id + "/preview/" + $scope.page.order);
    };

    $scope.publish = function() {
      $scope.saveCourse();
      $http.put("api/courses/" + $routeParams.courseId + "/publish").success(function(response) {
        $scope.course.published = response.published;
      });
    };

  }
]);