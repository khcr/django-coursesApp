import os

class TestRouter(object):
   
    def db_for_read(self, model, **hints):
        return TestRouter.test_db()

    def db_for_write(self, model, **hints):
        return TestRouter.test_db()

    def allow_relation(self, obj1, obj2, **hints):
        return TestRouter.test_db()

    def allow_migrate(self, db, model, **hints):
        return True 

    @staticmethod
    def test_db():
        try:
            env = os.environ['ENV']
        except KeyError:
            env = ""
        if env == "test":
            return "test"
        else:
            return None