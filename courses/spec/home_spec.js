describe('courses homepage', function() {
  beforeEach(function() {
    browser.get('http://localhost:3333/courses');
  });

  it('display a list of course', function() {
    

    expect(browser.getTitle()).toEqual('Cours');
  });
});