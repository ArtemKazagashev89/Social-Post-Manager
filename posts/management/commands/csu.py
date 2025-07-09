from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = "admin"
        password = "Admin1234!"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
