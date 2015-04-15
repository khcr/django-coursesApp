"use strict";

var app = angular.module("tags");

// change les balises Angular pour éviter les conflits avec Django
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol("{$");
  $interpolateProvider.endSymbol("$}");
});