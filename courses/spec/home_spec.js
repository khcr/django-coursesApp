"use strict";

describe("courses homepage", function() {
  beforeEach(function() {
    browser.get("http://localhost:3333/courses/#/");
  });

  it("displays a list of all courses", function() {
    var course = element.all(by.repeater("course in courses")).first();
    expect(course.getText()).toContain("Equations de droites");
  });

  it("displays different categories", function() {
    var categories = element(by.css(".categories"));
    expect(categories.getText()).toContain("Géométrie");
  });

  it("allows to click on a category", function() {
    element(by.id("favorites")).click();
    var courses = element(by.repeater("course in courses"));
    expect(courses.isPresent()).toBe(false);
  });

  it("redirects to a course", function() {
    var course = element.all(by.css(".course-block")).first();
    course.click();
    var title = element(by.binding("course.name"));
    expect(title.getText()).toEqual("Equations de droites");
  });
});