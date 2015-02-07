var app = angular.module('resources');

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

app.factory('Section', ['$resource', function($resource) {
  return $resource(
    'api/sections/:sectionId',
    {sectionId: '@id'}
  );
}]);

app.factory('Comment', ['$resource', function($resource) {
  return $resource(
    'api/courses/:courseId/comments/:commentId',
    {courseId: '@course_id', commentId: '@id'}
  );
}]);