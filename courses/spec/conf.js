// Configuration Protractor
exports.config = {
  seleniumAddress: 'http://localhost:4444/wd/hub',
  specs: ['*spec.js'],

  capabilities: {
    'browserName': 'chrome'
  },

  framework: 'jasmine2',

  jasmineNodeOpts: {
    showColors: true,
  },

  onPrepare: function() {
    global.login = require("./helpers/login_helper")
  }
}