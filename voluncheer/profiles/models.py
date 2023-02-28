from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserType(models.IntegerChoices):
    """Container for all possible user types."""
    ADMIN = 0, "Admin"
    ORGANIZATION = 1, "Organization"
    VOLUNTEER = 2, "Volunteer"


class UserManager(BaseUserManager):
    """UserManager allows the app to override the required username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("creating a user requires an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Creates and ordinary, everyday non-super user."""
        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Creates an Admin superuser."""
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["type"] = UserType.ADMIN

        if extra_fields.get("is_staff") is not True:
            raise ValueError("a superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("a superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """A User represents an abstract authenticated entity.

    Each user is associated with a particular Profile type
    (Volunteer|Organization) granting authorization to claim, modify, and delete
    the associated profile.

    Attributes:
        email: the unique email address associated with a particular user.
        password: the secret password to use during authentication.
    """
    username = None
    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    type = models.IntegerField(choices=UserType.choices)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    @property
    def is_organization(self):
        """Returns true if this user is associated with an organization."""
        return self.type == UserType.ORGANIZATION

    @property
    def is_volunteer(self):
        """Returns true if this user is associated with an volunteer."""
        return self.type == UserType.VOLUNTEER

    @property
    def is_admin(self):
        """Returns true if this user is an admin."""
        return self.type == UserType.ADMIN


class Organization(models.Model):
    """The Organization profile type.

    Attributes:
        user: the one-to-one mapping of an authenticated user.
        name: the official name of the organization.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    """The Volunteer profile type.

    Attributes:
        user: the one-to-one mapping of an authenticated user.
        first_name: the name given to an individual (often referred to as the
            first name in English speaking countries).
        last_name: the family name of an individual (often referred to as the
            last name in English speaking countries).
        date_of_birth: the birth date of an individual.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True, null=True)
    badges = models.CharField(max_length=1024, default="")

    BADGES = {
        "Badge 1": "images/badge-1.png",
        "Badge 2": "images/badge-2.png",
        "Badge 3": "images/badge-3.png",
        "Badge 4": "images/badge-4.png",
        "Badge 5": "images/badge-5.png",
        "Badge 6": "images/badge-6.png",
    }

    def __str__(self):
        return self.name

    @property
    def name(self):
        """Returns the full name of the volunteer."""
        return f"{self.first_name} {self.last_name}"
