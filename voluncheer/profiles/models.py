from datetime import timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


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
    (Volunteer|Organization) granting authorization to claim,
    modify, and delete the associated profile.

    Attributes:
        email: the unique email address associated with a particular user.
        password: the secret password to use during authentication.
    """

    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=254,
        unique=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    type = models.IntegerField(choices=UserType.choices)
    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

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

    # def get_absolute_url(self):
    #     return reverse('profile', args=[str(self.pk)])


def _profile_photo_path(instance, filename):
    if instance.user.is_organization:
        prefix = "organizations"
    elif instance.user.is_volunteer:
        prefix = "volunteers"
    elif instance.user.is_admin:
        prefix = "admins"
    else:
        raise ValueError(f"unsupported user type {instance.user.type}")
    return f"{prefix}/{instance.user.id}/{filename}"


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
    photo = models.ImageField(upload_to=_profile_photo_path, blank=True, null=True)
    website = models.CharField(max_length=200, default="")
    description = models.TextField(help_text="Introduce your organization here.", default="")

    def __str__(self):
        return self.name


class BadgeType(models.IntegerChoices):
    """Container for all possible badge types."""

    VOLUNTEER_HOURS_BADGE = 0, "VOLUNTEER_HOURS_BADGE"


def _badge_img_path(instance, filename):
    """Returns directory path for storing badge images"""
    return f"badges/{filename}"


class Badge(models.Model):
    """The Badge model for Volunteer achievements

    Attributes:
        name: the name of the badge.
        type: the type of the badge.
        img: the image associated with badge.
        hours_required: the amount of time required to earn the badge.

    """

    name = models.TextField(max_length=200)
    type = models.IntegerField(choices=BadgeType.choices)
    img = models.ImageField(upload_to=_badge_img_path)
    hours_required = models.DurationField()

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
    badges = models.ManyToManyField(Badge, related_name="badges", blank=True)
    photo = models.ImageField(upload_to=_profile_photo_path, blank=True, null=True)
    description = models.TextField(help_text="Introduce yourself here.", default="")
    hours_volunteered = models.DurationField(default=timedelta(days=0), null=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        """Returns the full name of the volunteer."""
        return f"{self.first_name} {self.last_name}"

    def award_volunteer_hours_badges(self):
        """
        Checks if a volunteer is eligible for any new volunteer level badges.
        If so, adds those badges to the volunteer.
        Returns hours remaining until next volunteer level badge.
        """
        badges = Badge.objects.filter(type=BadgeType.VOLUNTEER_HOURS_BADGE).order_by(
            "hours_required"
        )
        hours_remaining = None
        badge_added = False

        for badge in badges:
            if self.hours_volunteered >= badge.hours_required:
                self.badges.add(badge)
                badge_added = True
            else:
                duration_remaining = badge.hours_required - self.hours_volunteered
                hours_remaining = round(duration_remaining.total_seconds() / 3600, 2)
                break

        if badge_added:
            self.save()

        return hours_remaining
