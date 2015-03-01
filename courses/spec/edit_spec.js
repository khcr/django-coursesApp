"use strict";

describe("course edit", function() {
  beforeEach(function() {
    browser.get("http://localhost:3333/courses/#/1/edit");
  });

  it("allows to edit the course", function() {
    element(by.id("send-course")).click();
    expect(element(by.id("notice")).getText()).toEqual("Sauvegardé");
  });

});