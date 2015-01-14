var app = angular.module('coursesApp', ['ngResource', 'ngRoute', 'ngSanitize', 'ngAnimate', 'monospaced.elastic', 'angularFileUpload']);

app.config(function($routeProvider, $resourceProvider){
	var basePath = '/static/courses/html/';
	$routeProvider.when('/', {
			templateUrl: basePath + 'index.html',
			controller: 'HomeController'
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

app.controller('HomeController', ['$scope', '$location', 'Course', function($scope, $location, Course) {
	$scope.courses = Course.query();

	$scope.showCourse = function(course) {
		$location.path(course.id + "/view/1");
	};

}]);

app.controller('AboutController', function() {
	
});

app.controller('NewCourseController', ['$scope', '$location', '$http', 'Course', function($scope, $location, $http, Course) {
  $http.get('api/themes').success(function(themes) {
    $scope.themes = themes;
  });

	$scope.createCourse = function() {
		course = new Course($scope.course);
    course.$save(function(course) {
      $location.path(course.id + "/edit/1");
    });
	};
}]);

app.controller('EditCourseController', ['$scope', '$routeParams', '$location', '$upload', 'Section', '$filter', 'Page', 'Course',
  function($scope, $routeParams, $location, $upload, Section, $filter, Page, Course, Range) {

    $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
      $scope.course = new Course(page.course);
    });

    $scope.newSection = function() {
      $scope.page.$add_section()
    };
    $scope.removeSection = function(key) {
      section = new Section($scope.page.sections[key]);
      section.$delete(function() {
        $scope.page.sections.splice(key, 1);
      });
      // TODO: rewrite order
    };
    $scope.upSection = function(key) {
      $scope.page.sections[key].order -= 1
      $scope.page.sections[key - 1].order += 1
      $scope.page.$update({ objectId: $scope.course.id }, function() {
        alert('saved !');
      });
    };
    $scope.downSection = function(key) {
      if($scope.page.sections[key + 1])
      $scope.page.sections[key].order += 1
      $scope.page.sections[key + 1].order -= 1
      $scope.page.$update({ objectId: $scope.course.id }, function() {
        alert('saved !');
      });
      
    };
    $scope.saveCourse = function() {
      angular.forEach($scope.page.sections, function(value, key) {
        $scope.page.sections[key].html_content = $filter('markdown')($scope.page.sections[key].markdown_content)
      });
      $scope.page.$update({ objectId: $scope.course.id }, function() {
        alert('saved !');
      });
    };
    $scope.newPage = function() {
      // TODO: save course in the database and add a new page
      $scope.course.$add_page(function(page) {
        $scope.page = page;
        $scope.course = page.course;
        $location.path($scope.course.id + "/edit/" + $scope.page.order)
      });
      
    };
    $scope.isCurrentPage = function(number) {
      return number === $scope.page.id;
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

app.controller('PreviewCourseController', ['$scope', '$routeParams', 'Page', function($scope, $routeParams, Page) {
  $scope.page = Page.get({ pageId: $routeParams.pageId, objectId: $routeParams.courseId }, function(page) {
    $scope.course = page.course
  })
}]);

app.controller('ViewCourseController', ['$scope', '$routeParams', '$location', 'Page', function($scope, $routeParams, $location, Page) {
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
}]);
