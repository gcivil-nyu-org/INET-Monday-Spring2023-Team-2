"""The create_su command creates a new super user if one with the same email does not exist."""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from profiles.models import UserType


class Command(BaseCommand):
    help = "Creates a new super user if one with the provided email does not already exist."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            default="admin@admin.com",
            help="The email address of the super user to create.",
        )
        parser.add_argument(
            "--password",
            help="The password of the super user to create.",
        )

    def handle(self, *args, **options):
        del args  # Unused.
        User = get_user_model()
        email = options["email"]

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Super user with email address {repr(email)} already exists.")
            )
            return

        User.objects.create_superuser(
            email=email,
            password=options["password"],
            is_active=True,
            type=UserType.ADMIN,
        )
        self.stdout.write(self.style.SUCCESS(f"Successfully created super user for {repr(email)}."))
