MathJax.Hub.Config({

  skipStartupTypeset: true,
  showProcessingMessages: false,
  messageStyle: "none",
  showMathMenu: false,
  showMathMenuMSIE: false,

  tex2jax: {
    displayMath: [
      ['||','||'],
    ],
  },

  styles: {
    ".MathJax_Display": {
      clear: "both"
    }
  }

});

MathJax.Ajax.loadComplete("[MathJax]/config/local/local.js");
