from django.db import models
from datetime import datetime
import random


# Create your models here.

class Organization(models.Model):
    organization_name = models.CharField(max_length=256)
    organization_email = models.CharField(max_length=256, default="")
    organization_address_city = models.CharField(max_length=256, default="")
    organization_image = models.CharField(max_length=256, default="images/organize_image_unknown.png")
    organization_website = models.CharField(max_length=256, default="")

