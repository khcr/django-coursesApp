"use strict";

describe("courses homepage", function() {
  beforeEach(function() {
    browser.get("http://localhost:3333/courses/#/new");
  });

  it("displays the page", function() {
    expect(element(by.css("h1")).getText()).toEqual("Nouveau cours");
  });

  it("allows to create a new course", function() {
    var courseTitle = "Applications"
    element(by.model("course.name")).sendKeys(courseTitle);
    element(by.model("course.description")).sendKeys("Lorem ipsum dolorem ciceron.");
    element(by.model("course.chapter")).element(by.cssContainingText("option", "Les droites")).click();
    element.all(by.model("course.difficulty")).first().click();
    element(by.buttonText("Envoyer")).click();
    expect(element(by.css(".course-title")).getText()).toEqual(courseTitle);
  });

  it("validates the form", function() {
    expect(element(by.buttonText("Envoyer")).getAttribute("disabled")).toEqual("true");
  });

});