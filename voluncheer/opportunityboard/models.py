from django.db import models
from profiles.models import Organization


CATEGORIES = {
    ("community", "Community"),
    ("animals", "Animal"),
    ("environment", "Environment"),
    ("healthcare", "Healthcare"),
    ("sports", "Sports"),
}


class Opportunity(models.Model):
    """
    The Opportunity type.

    Attributes:
        organization: the many-to-one mapping of the organization.
        pubdate: when opportunity was published. *allowed to be blank for now
        category: the type of opportunity
        title: the name of the opportunity.
        description: a description of the opportunity.
        date: the date and start time of the opportunity.
        duration: the length of the opportunity, in hours and seconds.
        address_1: the location of the opportunity.
        address_2: reserved for an additional address field.
        longitude: used for mapping the opportunity. *allowed to be blank for now
        latitude: used for mapping the opportunity. *allowed to be blank for now
        staffing: the requested number of volunteers for the opportunity.
    """

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    pubdate = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    duration = models.DurationField()
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(null=True, blank=True, max_length=255)
    longitude = models.DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=6
    )
    latitude = models.DecimalField(
        null=True, blank=True, max_digits=9, decimal_places=6
    )
    staffing = models.IntegerField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
