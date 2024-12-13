from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    """Sets up periodic tasks for the application"""

    def handle(self, *args, **kwargs):

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES,
        )

        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Sync exchange rates from yahoo every 5 minutes',
            task='currencies.tasks.sync_exchange_rates_from_yahoo',
        )

        self.stdout.write(self.style.SUCCESS('Periodic tasks have been set up.'))
