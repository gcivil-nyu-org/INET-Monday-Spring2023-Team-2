from django.db import models
from profiles.models import Organization


CATEGORIES = {
    ("community", "Community"),
    ("animals", "Animal"),
    ("environment", "Environment"),
    ("healthcare", "Healthcare"),
    ("sports", "Sports"),
}


class Job(models.Model):
    """
    The Job type.

    Attributes:
        organization: the many-to-one mapping of the organization.
        pubdate: when job was published. *allowed to be blank for now
        category: the type of job
        title: the name of the job.
        description: a description of the job.
        date: the date and start time of the job.
        duration: the length of the job, in hours and seconds.
        address_1: the location of the job.
        address_2: reserved for an additional address field.
        longitude: used for mapping the job. *allowed to be blank for now
        latitude: used for mapping the job. *allowed to be blank for now
        staffing: the requested number of volunteers for the job.
    """

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    pubdate = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(null=True, blank=True, max_length=255)
    longitude = models.DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=6
    )
    latitude = models.DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=6
    )
    staffing = models.IntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
