# myapp/management/commands/load_custom_users.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
import json

class Command(BaseCommand):
    help = 'Load custom user data from a fixture'

    def handle(self, *args, **options):
        fixture_name = 'tutdb/fixtures/users.json'  # Replace with the actual fixture name
        call_command('loaddata', fixture_name, app_label='tutdb', verbosity=0)

        result = {"message": "Successfully Loading initial data"}

        return json.dumps(result)