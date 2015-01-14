(function(){
  var courses = function(converter) {
    return [
      //{ type: 'lang', regex: '\\|{2}[^\\|]+\\|{2}', replace: '<mathjax> || f(x) || </mathjax>' }
    ];
  };

  // Client-side export
  if (typeof window !== 'undefined' && window.Showdown && window.Showdown.extensions) { window.Showdown.extensions.courses = courses; }
}());