"use strict";

describe("course pages edit", function() {
  beforeEach(function() {
    browser.get("http://localhost:3333/courses/#/1/edit/1");
  });

  it("allows to create a new page", function() {
    element(by.id("new-page")).click();
    expect(element(by.model("page.name")).getAttribute("value")).toEqual("Titre de la page");
  });

  it("allows to move a section", function() {
    var name = element.all(by.model("section.name")).last().getAttribute("value");
    element.all(by.css(".up-section")).then(function(elements) {
      elements[elements.length - 1].click();
    }).then(function() {
      element.all(by.model("section.name")).then(function(elements) {
        expect(elements[elements.length - 2].getAttribute("value")).toEqual(name);
      });
    });
  });

  it("allows to delete a section", function() {
    element.all(by.css(".sections")).then(function(elements) {
      return elements.length - 1;
    }).then(function(count) {
      element.all(by.css(".remove-section")).then(function(elements) {
        elements[0].click();
      }).then(function() {
        expect(element.all(by.css(".sections")).count()).toEqual(count);
      });
    });
  });

  it("allows to create a new section", function() {
    element.all(by.css(".sections")).then(function(elements) {
      return elements.length + 1;
    }).then(function(count) {
      element(by.id("new-section")).click();
      expect(element.all(by.css(".sections")).count()).toEqual(count);
    });
  });

  it("allows to save the page", function() {
    var date = element(by.id("last-save")).getText();
    element(by.id("save-page")).click();
    browser.sleep(1000);
    expect(element(by.id("last-save")).getText()).not.toEqual(date);
  });

  it("allows to (un)publish the course", function() {
    expect(element(by.id("unpublish-course")).isDisplayed()).toBeTruthy();
    element(by.id("unpublish-course")).click();
    expect(element(by.id("publish-course")).isDisplayed()).toBeTruthy();
  });

  it("allows to make a preview", function() {
    element(by.id("preview-page")).click();
    expect(element(by.binding("page.name")).getText()).toEqual("Généralité");
  });

});