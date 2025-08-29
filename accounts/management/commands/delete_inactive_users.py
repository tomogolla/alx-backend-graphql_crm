from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Delete users inactive for more than 30 days"

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=30)
        inactive_users = User.objects.filter(last_login__lt=cutoff_date)

        count = inactive_users.count()
        inactive_users.delete()

        self.stdout.write(self.style.SUCCESS(f"Deleted {count} inactive users."))
