import time
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OperationalError

from django.core.management import call_command
from django.db.utils import OperationalError as DjangoOperationalError
from django.test import SimpleTestCase


# @patch is used to mock classes or methods in order to isolate behavior during testing. In this case, we are mocking
# the `check` method of the `Command` class from the `wait_for_db` management command.
@patch('core.management.commands.wait_for_db.Command.check')
class WaitForDbTest(SimpleTestCase):

    def test_wait_for_db_ready(self, mocked_check):
        mocked_check.return_value = True

        call_command('wait_for_db')

        mocked_check.assert_called_once_with(databases=['default'])

    # Mocking time.sleep to avoid actual delays during tests, since we are going to sleep before checking again
    @patch('time.sleep')
    def test_wait_for_db_not_ready(self, mocked_sleep, mocked_check):
        # We actually don't need to mock the return value of sleep. Simply mocking the method is sufficient

        # Simulate the database not being ready by raising OperationalErrors multiple times
        mocked_check.side_effect = [Psycopg2OperationalError] * 2 + [DjangoOperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(mocked_check.call_count, 6)  # We throw 5 errors before success
        mocked_check.assert_called_with(databases=['default'])
