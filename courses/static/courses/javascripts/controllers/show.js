var app = angular.module('controllers');

app.controller('ShowCourseController', ['$scope', '$routeParams', '$location', 'Page', 'Comment', '$http', '$anchorScroll', '$timeout', function($scope, $routeParams, $location, Page, Comment, $http, $anchorScroll, $timeout) {
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

  $scope.comments = Comment.query({courseId: $routeParams.courseId});

  var newComment = new Comment({"placeholder":"Ton commentaire", "user":"Keran", course_id: $routeParams.courseId});
  $scope.comment = Object.create(newComment);

  $scope.saveComment = function() {
    $scope.comment.$save(function(comment) {
      $scope.comments.push(comment);
      $scope.comment = Object.create(newComment);
    });
  };

  $scope.showComments = false;

  $scope.toggleComments = function() {
    $scope.showComments = !$scope.showComments;
  };

  $http.get('api/courses/' + $routeParams.courseId + '/menu').success(function(pages) {
    $scope.pages = pages;
  });

  $scope.isCurrentPage = function(page) {
    return page.order === $scope.page.order
  };

  $scope.isProgress = function(name) {
    return $scope.page.progression === name;
  };

  $scope.saveProgress = function(isDone) {
    $http.post('api/pages/' + $scope.page.id + '/progression', {is_done: isDone}).
      success(function(response) {
        if( !$scope.lastPage() ) {
          $scope.nextPage();
        } else {
          $scope.page.progression = response.progression;
          $scope.page.course.percentage = response.percentage;
        }
      })
  };

}]);