from django.db import models


class Job(models.Model):
    organization = models.ForeignKey("profiles.Organization", on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    pubdate = models.DateTimeField('date published')
    description = models.CharField(max_length=1024)
    location = models.CharField(max_length=256)
    worktime = models.CharField(max_length=256, default="Not Specified")
    image = models.CharField(max_length=256)
