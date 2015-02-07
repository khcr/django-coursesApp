// Main module 
angular.module('coursesApp', ['ngSanitize', 'ngAnimate', 'monospaced.elastic', 'controllers', 'routes', 'resources', 'filters', 'directives']);
// define modules
angular.module('controllers', ['angularFileUpload']);
angular.module('resources', ['ngResource'])
angular.module('directives', []);
angular.module('filters', []);
angular.module('routes', ['ngRoute', 'ngResource']);