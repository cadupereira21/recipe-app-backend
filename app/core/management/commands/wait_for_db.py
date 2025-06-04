"""Because of the structure of this Django project, the main app manage.py file is going to be able to use this file
as a management command."""
import time

from psycopg2 import OperationalError as Psycopg2OperationalError

from django.db.utils import OperationalError as DjangoOperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    # Wait for the database to be available.

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database')

        db_up = False

        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OperationalError, DjangoOperationalError) as e:
                self.stdout.write(self.style.ERROR(f'Database unavailable, trying again in 1 second'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is available!'))