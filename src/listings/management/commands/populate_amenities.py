from django.core.management.base import BaseCommand
from listings.models import Amenity
from listings.choices import common_amenities


class Command(BaseCommand):
    help = 'Populate the database with common property amenities'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate amenities...')
        
        created_count = 0
        for amenity_data in common_amenities:
            amenity, created = Amenity.objects.get_or_create(
                name=amenity_data['name'],
                defaults={'icon': amenity_data['icon']}
            )
            if created:
                created_count += 1
                self.stdout.write(f'Created amenity: {amenity.name}')
            else:
                self.stdout.write(f'Amenity already exists: {amenity.name}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated {created_count} new amenities. '
                f'Total amenities in database: {Amenity.objects.count()}'
            )
        ) 