var app = angular.module('controllers');

app.controller('EditCourseController', ['$scope', '$routeParams', '$location', '$upload', 'Section', '$filter', 'Page', 'Course', '$interval', '$http',
  function($scope, $routeParams, $location, $upload, Section, $filter, Page, Course, $interval, $http) {

    $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
      $scope.course = new Course(page.course);
    });

    $scope.newSection = function() {
      $scope.saveCourse();
      $scope.page.$add_section()
    };
    $scope.removeSection = function(key) {
      $scope.saveCourse();
      for(var i = key + 1; i < $scope.page.sections.length; i++) {
        $scope.page.sections[i].order -= 1;
      }
      section = new Section($scope.page.sections[key]);
      section.$delete(function() {
        $scope.page.sections.splice(key, 1);
        $scope.page.$update({ objectId: $scope.course.id });
      });
    };
    $scope.upSection = function(key) {
      $scope.saveCourse();
      if(key !== 0) {
        $scope.page.sections[key].order -= 1;
        $scope.page.sections[key - 1].order += 1;
        $scope.page.$update({ objectId: $scope.course.id });
      }
    };
    $scope.downSection = function(key) {
      $scope.saveCourse();
      if($scope.page.sections[key + 1] !== undefined) {
        $scope.page.sections[key].order += 1;
        $scope.page.sections[key + 1].order -= 1;
        $scope.page.$update({ objectId: $scope.course.id });
      }
    };
    $scope.saveCourse = function() {
      angular.forEach($scope.page.sections, function(value, key) {
        $scope.page.sections[key].html_content = $filter('markdown')($scope.page.sections[key].markdown_content)
      });
      $scope.page.$update({ objectId: $scope.course.id }, function() {
        $scope.lastSave = new Date;
      });
    };

    var interval = $interval($scope.saveCourse, 30000);
    $scope.lastSave = new Date;

    $scope.$on("$destroy", function(){
      $interval.cancel(interval);
      $scope.saveCourse();
    });

    $scope.newPage = function() {
      $scope.saveCourse();
      $scope.course.$add_page(function(page) {
        $scope.page = page;
        $scope.course = page.course;
        $location.path($scope.course.id + "/edit/" + $scope.page.order)
      });
      
    };
    $scope.isCurrentPage = function(number) {
      return number === $scope.page.id;
    };
    $scope.preview = function() {
      $scope.saveCourse();
      $location.path($scope.course.id + "/preview/" + $scope.page.order);
    };

    $scope.publish = function() {
      $scope.saveCourse();
      $http.put("api/courses/" + $routeParams.courseId + "/publish").success(function(response) {
        $scope.course.published = !$scope.course.published
      });
    };

    $scope.onFileSelect = function($files) {
      for (var i = 0; i < $files.length; i++) {
        var file = $files[i];
        $scope.upload = $upload.upload({
          url: '/upload',
          method: 'POST',
          file: file
        }).progress(function(evt) {
          console.log('percent: ' + parseInt(100.0 * evt.loaded / evt.total));
        }).success(function(data, status, headers, config) {
          console.log("success");
        }).error(function() {
          console.log("error");
        });
      }
    };
  }
]);