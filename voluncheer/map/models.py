from django.db import models


# Create your models here.
class NYCharities(models.Model):
    class Meta:
        verbose_name_plural = "NYCharities"

    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    type = models.CharField(max_length=255)
    bin_num = models.PositiveBigIntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
