import time
import os
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Watch a CSV file for changes and auto-import follow-ups'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str, required=True, help='Path to the CSV file')
        parser.add_argument('--username', type=str, required=True, help='Username to associate follow-ups with')
        parser.add_argument('--interval', type=int, default=2, help='Check interval in seconds (default: 2)')

    def handle(self, *args, **options):
        csv_file = options['csv']
        username = options['username']
        interval = options['interval']

        if not os.path.exists(csv_file):
            raise CommandError(f'CSV file "{csv_file}" does not exist')

        self.stdout.write(self.style.SUCCESS(f'Watching "{csv_file}" for changes...'))
        self.stdout.write('Press Ctrl+C to stop.\n')

        last_modified = os.path.getmtime(csv_file)
        
        # Initial import
        self.stdout.write('Running initial import...')
        try:
            call_command('import_followups', csv=csv_file, username=username, update=True)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Import error: {e}'))

        try:
            while True:
                time.sleep(interval)
                current_modified = os.path.getmtime(csv_file)
                
                if current_modified != last_modified:
                    last_modified = current_modified
                    self.stdout.write(f'\nFile changed at {time.strftime("%H:%M:%S")}. Importing...')
                    try:
                        call_command('import_followups', csv=csv_file, username=username, update=True)
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Import error: {e}'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nStopped watching.'))
