# http://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
from django.core.management.base import BaseCommand, CommandError
import subprocess
import os 
import signal
from django.conf import settings

class Command(BaseCommand):
    args = '<specs>'
    help = 'Run the tests'

    def handle(self, *args, **options):
        os.environ['WEBMATH_ENV'] = 'test'
        # ask the app
        directory = input("\nIn which app would you like to run the tests? [default: courses]\n") or "courses"
        if directory not in settings.INSTALLED_APPS:
            raise CommandError("App '{}'' does not exist".format(directory))

        self.stdout.write('\n### SERVERS ###\n\n')
        server = subprocess.Popen(["python3", "manage.py", "runserver", "3333"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
        webdriver = subprocess.Popen(["webdriver-manager", "start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
        self.stdout.write('servers launched\n')

        # create the database
        self.stdout.write('\n### DATABASE SETUP ###\n\n')
        subprocess.call(["python3", "manage.py", "migrate", "--database=test"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.stdout.write('database created\n')

        # init the demo data
        subprocess.call(["python3", "manage.py", "seed"])

        # run the tests
        self.stdout.write('\n### TESTS ###\n\n')
        cmd = ["protractor", directory + "/spec/conf.js"]
        if args:
            cmd = cmd + ["--specs", "{}/spec/{}".format(directory, args[0])]
        subprocess.call(cmd)

        # remove the database
        subprocess.call(["rm", "test.sqlite3"])

        # close servers
        os.killpg(webdriver.pid, signal.SIGTERM)
        os.killpg(server.pid, signal.SIGTERM)
        self.stdout.write('\nservers closed\n\n')

        os.environ['WEBMATH_ENV'] = 'development'