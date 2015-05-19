"use strict";

// affiche une page 404 si une ressource n'a pas été trouvée
angular.module("Interceptors", []).factory('NotFoundInterceptor', function($q, $location) {
    return {        
        'responseError': function(rejection) {
            if(rejection.status === 404) {
                $location.path("404");
            }
            return $q.reject(rejection);
        }
    }
}).config(function($provide, $httpProvider) {
    $httpProvider.interceptors.push('NotFoundInterceptor')
});