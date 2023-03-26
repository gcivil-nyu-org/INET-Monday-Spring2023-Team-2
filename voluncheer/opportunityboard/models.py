from django.db import models

from profiles.models import Organization

FREQUENCIES = [("weekly", "Weekly")]


class Category(models.Model):
    """A category of an opportunity"""

    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """A subcategory of an opportunity"""

    class Meta:
        verbose_name_plural = "subcategories"

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subsubcategory(models.Model):
    """A sub-subcategory of an opportunity"""

    class Meta:
        verbose_name_plural = "subsubcategories"

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


def _opportunity_photo_path(instance, filename):
    return f"opportunities/{instance.organization.user.id}/{filename}"


class Opportunity(models.Model):
    """
    The Opportunity type.

    Attributes:
        organization: the many-to-one mapping of the organization.
        pubdate: when opportunity was published. *allowed to be blank for now
        category: the type of opportunity
        subcategory: the type of opportunity
        subsubcategory: the type of opportunity
        title: the name of the opportunity.
        description: a description of the opportunity.
        date: the date and start time of the opportunity.
        end: the end time of the opportunity.
        is_recurring: denotes whether the opportunity is recurring.
        recurrence: the frequency of recurrences.
        end_date: the date a recurring opportunity ends.
        address_1: the location of the opportunity.
        address_2: reserved for an additional address field.
        longitude: used for mapping the opportunity. *allowed to be blank for now
        latitude: used for mapping the opportunity. *allowed to be blank for now
        staffing: the requested number of volunteers for the opportunity.
    """

    class Meta:
        verbose_name_plural = "opportunities"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    pubdate = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, blank=True, null=True)
    subsubcategory = models.ForeignKey(
        Subsubcategory, on_delete=models.SET_NULL, blank=True, null=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    end = models.TimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence = models.CharField(max_length=6, choices=FREQUENCIES, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(null=True, blank=True, max_length=255)
    longitude = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    latitude = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=6)
    staffing = models.PositiveIntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    photo = models.ImageField(upload_to=_opportunity_photo_path, blank=True, null=True)

    def __str__(self):
        return self.title
