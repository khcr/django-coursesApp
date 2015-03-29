# Routeur Django pour indiquer quelle base de données utiliser
# ce router indique s'il faut utiliser la base de données de test ou la normale
import os

class TestRouter(object):
   
    def db_for_read(self, model, **hints):
        return TestRouter.test_db()

    def db_for_write(self, model, **hints):
        return TestRouter.test_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True 

    def allow_migrate(self, db, model, **hints):
        return True 

    @staticmethod
    def test_db():
        # voir la commande de tests dans courses/management/commands/tests.py
        # on y assigne une variable d'environnement pour indiquer que les tests sont en cours
        try:
            # variable d'environnement
            env = os.environ['WEBMATH_ENV']
        except KeyError:
            env = ""
        # teste si l'application est en environnement de test
        if env == "test":
            return "test"
        else:
            return None