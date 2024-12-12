from django.conf import settings
from django.core.management.base import BaseCommand

from currencies.models import Currency


class Command(BaseCommand):
    """Django command to create currencies declared in settings"""

    def handle(self, *args, **options):
        self.stdout.write('Creating currencies...')
        for currency in settings.CURRENCIES:
            currency, created = Currency.objects.get_or_create(ticker=currency)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Currency: {currency} created.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Currency: {currency} already exists.'))

        self.stdout.write(self.style.SUCCESS('Done.'))
