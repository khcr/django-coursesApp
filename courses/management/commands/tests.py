# http://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
from django.core.management.base import BaseCommand, CommandError
import subprocess
import os 
import signal
from optparse import make_option

from django.conf import settings

class Command(BaseCommand):
    args = '<specs>'
    help = 'Lance les tests'
    option_list = BaseCommand.option_list + (
        make_option('--app',
            dest='directory',
            default="courses",
            help='Spécifier l\'application pour lancer les tests'),
        )

    def handle(self, *args, **options):
        try:
            # change la variable d'environnement
            # voir webmath/test_router.py
            os.environ['WEBMATH_ENV'] = 'test'

            # teste si le dossier, l'application existe
            directory = options['directory']
            if directory not in settings.INSTALLED_APPS:
                raise CommandError("L'application '{}' n'existe pas".format(directory))

            # teste si le fichier spécifié existe
            if args and not os.path.isfile("{}/spec/{}".format(directory, args[0])): 
                raise CommandError("Le fichier spec '{}' n'existe pas".format(args[0]))

            self.stdout.write('\nlance les tests dans le dossier {} (utilisez l\'option --app pour changer ce comportement)\n'.format(directory))

            # lance les serveur Django et Webdriver
            server = subprocess.Popen(["python3", "manage.py", "runserver", "3333"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
            webdriver = subprocess.Popen(["webdriver-manager", "start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
            self.stdout.write('\n# SERVEURS: serveurs Django et Webdriver lancés\n')

            # crée la base de données de test
            self.stdout.write('\n# BASE DE DONNEES\n\n')
            subprocess.call(["python3", "manage.py", "migrate", "--database=test"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.stdout.write('base de données créée\n')

            # crée les données de démonstration
            subprocess.call(["python3", "manage.py", "seed"])

            # lance les tests
            self.stdout.write('\n# TESTS\n\n')
            cmd = ["protractor", directory + "/spec/conf.js"]
            # utilise un fichier spécifique si donné
            if args:
                cmd = cmd + ["--specs", "{}/spec/{}".format(directory, args[0])]
            subprocess.call(cmd)

            # supprime la base de données de test
            subprocess.call(["rm", "test.sqlite3"])
            self.stdout.write('\n# BASE DE DONNEES: nettoyée\n')

            # ferme les serveurs Django et Webdriver
            os.killpg(webdriver.pid, signal.SIGTERM)
            os.killpg(server.pid, signal.SIGTERM)
            self.stdout.write('\n# SERVEURS: serveurs Django et Webdriver fermés\n\n')

            # change la variable d'environnement
            os.environ['WEBMATH_ENV'] = 'development'
        # assure une interruption propre
        except KeyboardInterrupt:
            self.stdout.write('\n\n...Tests interrompus...')

            # change la variable d'environnement
            os.environ['WEBMATH_ENV'] = 'development'

            # ferme les serveurs
            if webdriver:
                os.killpg(webdriver.pid, signal.SIGTERM)
            if server:
                os.killpg(server.pid, signal.SIGTERM)
            self.stdout.write('\n# SERVEURS: serveurs Django et Webdriver fermés\n')

            # supprime la base de données
            if os.path.isfile("test.sqlite3"): 
                subprocess.call(["rm", "test.sqlite3"])
                self.stdout.write('\n# BASE DE DONNEES: nettoyée\n')
