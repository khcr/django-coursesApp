var app = angular.module('routes');

app.config(function($routeProvider, $resourceProvider){
  var basePath = '/static/courses/html/';
  $routeProvider.when('/', {
      templateUrl: basePath + 'index.html',
      controller: 'HomeCourseController'
    })
    .when('/about', {
      templateUrl: basePath + 'about.html',
      controller: 'AboutController'
    })
    .when('/new', {
      templateUrl: basePath + 'new.html',
      controller: 'NewCourseController'
    })
    .when('/:courseId/view/:pageId', {
      templateUrl: basePath + 'show.html',
      controller: 'ViewCourseController'
    })
    .when('/:courseId/edit/:pageId', {
      templateUrl: basePath + 'edit.html',
      controller: 'EditCourseController'
    })
    .when('/:courseId/preview/:pageId', {
      templateUrl: basePath + 'preview.html',
      controller: 'PreviewCourseController'
    })
    .otherwise({
      templateUrl: basePath + '404.html'
    });
    $resourceProvider.defaults.stripTrailingSlashes = true;
});