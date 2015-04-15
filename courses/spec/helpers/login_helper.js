module.exports = {
  asStudent: function () {
    browser.ignoreSynchronization = true;
    browser.get("http://localhost:3333/login");
    element(by.id('id_username')).sendKeys('dupont.alfred');
    element(by.id('id_password')).sendKeys('12341');
    element(by.buttonText("Connexion")).click();
    browser.ignoreSynchronization = false;
  },
  asTeacher: function() {
    browser.ignoreSynchronization = true;
    browser.get("http://localhost:3333/login");
    element(by.id('id_username')).sendKeys('smith.john');
    element(by.id('id_password')).sendKeys('12341');
    element(by.buttonText("Connexion")).click();
    browser.ignoreSynchronization = false;
  }
};