"use strict";

// https://docs.angularjs.org/guide/directive

var app = angular.module("directives");

// directive qui formate son contenu avec MathJax
app.directive("mathjax", ["$timeout", function($timeout) {
  return {
    restrict: "AE",
    template: "<div class='ng-hide' ng-transclude></div>",
    transclude: true,
    link: function(scope, element, attrs) {
      $timeout(function () {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub, element[0]]);
        MathJax.Hub.Queue(function() {
          element.children().removeClass("ng-hide");
        });
      });
    }
  };
}]);

// directive qui affiche un formulaire pour les informations de base d'un cours
app.directive("courseForm", function() {
  return {
    restrict: "E",
    templateUrl: "/static/courses/html/directives/course_form.html"
  };
});

// directive qui affiche un bouton pour retourner à l'édition d'un cours
app.directive("backToCourse", function() {
  return {
    restrict: "E",
    templateUrl: "/static/courses/html/directives/back_course.html"
  };
});
