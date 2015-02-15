var app = angular.module('filters');

app.filter('range', function() {
  return function(input, min, max) {
    min = parseInt(min);
    max = parseInt(max) + 1;
    for (var i=min; i<max; i++)
      input.push(i);
    return input;
  };
});

app.filter('markdown', function() {
  return function(input) {
    var converter = new Showdown.converter({ extensions: ['courses'] });
    return converter.makeHtml(input);
  };
});

app.filter('parameterize', function() {
  return function(input) {
    input = input || '';
    return input.replace(/\s/g, "_").toLowerCase();
  };
});