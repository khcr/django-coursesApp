// https://docs.angularjs.org/guide/module

// Application principale et ses dépendances
angular.module('coursesApp', ['ngSanitize', 'ngAnimate', 'monospaced.elastic', 'controllers', 'routes', 'resources', 'filters', 'directives']);

// définit les modules
angular.module('controllers', []);
angular.module('resources', ['ngResource']);
angular.module('directives', []);
angular.module('filters', []);
angular.module('routes', ['ngRoute', 'ngResource']);