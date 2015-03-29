"use strict";

// https://docs.angularjs.org/api/ng/filter/filter

var app = angular.module("filters");

// génère une liste de nombres entiers entre un minimum et un maximum
app.filter("range", function() {
  return function(input, min, max) {
    min = parseInt(min);
    max = parseInt(max) + 1;
    for (var i=min; i<max; i++)
      input.push(i);
    return input;
  };
});

// convertit une chaine de Markdown à HTML
// utilise Showdown.js
app.filter("markdown", function() {
  return function(input) {
    var converter = new Showdown.converter({ extensions: ["courses"] });
    return converter.makeHtml(input);
  };
});

// remplace les espaces par des underscores et enlève les majuscules
// pour formater une URL par exemple
app.filter("parameterize", function() {
  return function(input) {
    input = input || "";
    return input.replace(/\s/g, "_").toLowerCase();
  };
});