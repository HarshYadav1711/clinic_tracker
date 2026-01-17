import csv
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from followups.models import FollowUp


class Command(BaseCommand):
    help = 'Import follow-ups from a CSV file'

    # Fields that are auto-managed and should not be imported from CSV
    EXCLUDED_FIELDS = {'id', 'clinic', 'created_by', 'public_token', 'created_at', 'updated_at', 'status'}
    
    # Fields that have default values
    FIELD_DEFAULTS = {
        'language': 'en',
        'status': 'pending',
    }

    def add_arguments(self, parser):
        parser.add_argument('--csv', type=str, required=True, help='Path to the CSV file')
        parser.add_argument('--username', type=str, required=True, help='Username to associate follow-ups with')
        parser.add_argument('--update', action='store_true', help='Update existing records based on phone number')

    def get_model_fields(self):
        """Get all field names from the FollowUp model that can be imported."""
        return {
            field.name for field in FollowUp._meta.get_fields() 
            if hasattr(field, 'column') and field.name not in self.EXCLUDED_FIELDS
        }

    def handle(self, *args, **options):
        csv_file = options['csv']
        username = options['username']
        update_existing = options.get('update', False)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist')

        try:
            clinic = user.userprofile.clinic
        except AttributeError:
            raise CommandError(f'User "{username}" does not have a clinic profile')

        # Get valid model fields
        model_fields = self.get_model_fields()

        created_count = 0
        updated_count = 0
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            csv_fields = set(reader.fieldnames) if reader.fieldnames else set()
            
            # Find which CSV fields match model fields
            valid_fields = csv_fields & model_fields
            ignored_fields = csv_fields - model_fields
            
            if ignored_fields:
                self.stdout.write(self.style.WARNING(f'Ignoring CSV fields not in model: {", ".join(ignored_fields)}'))
            
            self.stdout.write(f'Importing fields: {", ".join(valid_fields)}')

            for row in reader:
                # Build data dict dynamically from CSV fields that match model fields
                data = {}
                for field in valid_fields:
                    value = row.get(field, '').strip() if row.get(field) else ''
                    if value or field not in self.FIELD_DEFAULTS:
                        data[field] = value if value else self.FIELD_DEFAULTS.get(field, '')
                    else:
                        data[field] = self.FIELD_DEFAULTS.get(field, '')

                phone = data.get('phone', '')
                if not phone:
                    self.stdout.write(self.style.WARNING('Skipping row with empty phone'))
                    continue

                if update_existing:
                    # Update or create based on phone number within the clinic
                    existing = FollowUp.objects.filter(clinic=clinic, phone=phone).first()
                    if existing:
                        # Update existing record with all valid fields
                        for field, value in data.items():
                            if field != 'phone':  # Don't update the key field
                                setattr(existing, field, value)
                        existing.save()
                        updated_count += 1
                    else:
                        FollowUp.objects.create(
                            clinic=clinic,
                            created_by=user,
                            status='pending',
                            **data
                        )
                        created_count += 1
                else:
                    FollowUp.objects.create(
                        clinic=clinic,
                        created_by=user,
                        status='pending',
                        **data
                    )
                    created_count += 1

        if update_existing:
            self.stdout.write(self.style.SUCCESS(f'Successfully imported: {created_count} created, {updated_count} updated'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {created_count} follow-ups'))