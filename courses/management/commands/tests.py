from django.core.management.base import BaseCommand, CommandError
import subprocess
import os 
from django.conf import settings

class Command(BaseCommand):
    help = 'Run the tests'

    def handle(self, *args, **options):
        os.environ["WEBMATH_ENV"] = 'test'
        # ask the app
        directory = input("In which app would you like to run the tests? [default: courses]\n") or "courses"
        if directory not in settings.INSTALLED_APPS:
            raise CommandError("App '{}'' does not exist".format(directory))
        # create the database
        self.stdout.write('\n### DATABASE SETUP ###\n\n')
        subprocess.call(["python3", "manage.py", "migrate", "--database=test"])
        # init the demo data
        subprocess.call(["python3", "manage.py", "seed"])
        # run the tests
        self.stdout.write('\n### TESTS ###\n\n')
        subprocess.call(["protractor", directory + "/spec/conf.js"])
        # remove the database
        subprocess.call(["rm", "test.sqlite3"])
        os.environ["WEBMATH_ENV"] = 'develepment'