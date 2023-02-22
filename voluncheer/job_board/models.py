from django.db import models
from datetime import datetime
import random

# Create your models here.

class Job(models.Model):
    job_organization = models.ForeignKey("organization_profile.Organization", on_delete=models.CASCADE)
    job_title = models.CharField(max_length=256)
    job_pubdate = models.DateTimeField('date published')
    job_discription = models.CharField(max_length=1024)
    job_location = models.CharField(max_length=256)
    job_worktime = models.CharField(max_length=256, default="Not Specified")
    job_image = models.CharField(max_length=256)