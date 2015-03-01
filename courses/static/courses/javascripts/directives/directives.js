"use strict";

var app = angular.module("directives");

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

app.directive("courseForm", function() {
  return {
    restrict: "E",
    templateUrl: "/static/courses/html/directives/course_form.html"
  };
});

app.directive("backToCourse", function() {
  return {
    restrict: "E",
    templateUrl: "/static/courses/html/directives/back_course.html"
  };
});
