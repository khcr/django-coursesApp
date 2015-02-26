"use strict";

describe("course show", function() {
  beforeEach(function() {
    browser.get("http://localhost:3333/courses/#/1/view/1");
  });

  it("displays the course", function() {
    expect(element(by.binding("course.name")).getText()).toEqual("Equations de droites");
    expect(element.all(by.binding("page.name")).first().getText()).toEqual("Généralité");
    var section = element.all(by.repeater("section in page.sections")).first();
    expect(section.element(by.binding("section.name")).getText()).toEqual("Lorem ipsum");
    expect(section.element(by.binding("section.html_content")).getText()).toContain("Mauris varius");
  });

  it("displays a menu", function() {
    var menu = element(by.css(".menu"));
    expect(menu.getText()).toContain("Lorem ipsum");
    expect(menu.getText()).toContain("Généralité");
  });

  it("allows to navigate from the menu", function() {
    element(by.css(".menu")).all(by.binding("page.name")).last().click();
    expect(element.all(by.binding("page.name")).first().getText()).toEqual("Les équations");
  });

  it("allows to switch pages", function() {
    element(by.id("next-page")).click();
    expect(element.all(by.binding("page.name")).first().getText()).toEqual("Les équations");
    element(by.id("previous-page")).click();
    expect(element.all(by.binding("page.name")).first().getText()).toEqual("Généralité");
  });

  it("allows to mark a successful page", function() {
    element(by.id("page-success")).click();
    expect(element.all(by.binding("page.name")).first().getText()).toEqual("Les équations");
    expect(element(by.css(".progress-bar")).getText()).toContain("50%");
  });

  it("allows to mark a not understood page", function() {
    element(by.id("page-defeat")).click();
    expect(element.all(by.binding("page.name")).first().getText()).toEqual("Les équations");
    expect(element(by.css(".progress-bar")).getText()).toContain("0%");
  });

  it("allows to mark a favorite course", function() {
    var star = element(by.css(".favorite"));
    star.click();
    expect(star.getAttribute("class")).not.toContain("glyphicon-star-empty");
    star.click();
    expect(star.getAttribute("class")).toContain("glyphicon-star-empty");
  });

  it("allows to post a comment", function() {
    var text = "J'ai adoré ce cours";
    element(by.id("show-comments")).click();
    element(by.model("comment.content")).sendKeys(text);
    element(by.id("submit-comment")).click();
    expect(element(by.repeater("comment in comments")).getText()).toContain(text);
  });

  it("previews the comment", function() {
    var text = "J'ai adoré ce cours";
    element(by.id("show-comments")).click();
    element(by.model("comment.content")).sendKeys(text);
    expect(element(by.binding("comment.content")).getText()).toEqual(text);
  });
});