import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from followups.models import FollowUp


class Command(BaseCommand):
    help = 'Import follow-ups from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str, required=True, help='Path to the CSV file')
        parser.add_argument('--username', type=str, required=True, help='Username to associate follow-ups with')

    def handle(self, *args, **options):
        csv_file = options['csv']
        username = options['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        try:
            clinic = user.userprofile.clinic
        except AttributeError:
            raise CommandError(f'User "{username}" does not have a clinic profile')

        count = 0
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            for row in reader:
                FollowUp.objects.create(
                    clinic=clinic,
                    created_by=user,
                    patient_name=row.get('patient_name', ''),
                    phone=row.get('phone', ''),
                    due_date=row.get('due_date'),
                    notes=row.get('notes') or '',
                    language=row.get('language', 'en'),
                    status='pending',
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} follow-ups'))