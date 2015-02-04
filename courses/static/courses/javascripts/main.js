var app = angular.module('coursesApp', ['ngResource', 'ngRoute', 'ngSanitize', 'ngAnimate', 'monospaced.elastic', 'angularFileUpload', 'controllers', 'routes']);
angular.module('controllers', [])

app.factory('Course', ['$resource', function($resource) {
  return $resource(
    'api/courses/:courseId/:resource',
    {courseId: '@id'},
    {
      add_page: { method: 'POST', params: { resource: 'pages' }}
    }
  );
}]);

app.factory('Page', ['$resource', function($resource) {
  return $resource(
    'api/pages/:pageId/:resource/:objectId',
    {pageId: '@id', resource: 'courses'},
    {
      update: { method: 'PUT' },
      add_section: { method: 'POST', params: {resource: 'sections' }}
    }
  );
}]);

app.filter('range', function() {
  return function(input, min, max) {
    min = parseInt(min);
    max = parseInt(max) + 1;
    for (var i=min; i<max; i++)
      input.push(i);
    return input;
  };
});

app.factory('Section', ['$resource', function($resource) {
  return $resource(
    'api/sections/:sectionId',
    {sectionId: '@id'}
  );
}]);


app.filter('markdown', function() {
  return function(input) {
    var converter = new Showdown.converter({ extensions: ['courses'] });
    return converter.makeHtml(input);
  };
});

app.directive('mathjax', ['$timeout', function($timeout) {
  return {
    restrict: 'AE',
    template: '<div class="ng-hide" ng-transclude></div>',
    transclude: true,
    link: function(scope, element, attrs) {
      $timeout(function () {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub, element[0]]);
        MathJax.Hub.Queue(function() {
          element.children().removeClass("ng-hide");
        })
      });
    }
  };
}]);
