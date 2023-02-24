from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLE_CHOICES = (
    (1,'Volunteer'),
    (2,'Organization'),
)

class User(AbstractUser):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    date_of_birth = models.DateField(blank = True, null = True) 
    email = models.EmailField(max_length = 254, unique = True)
    password = models.CharField(max_length = 127)

    is_admin = models.BooleanField(default = False)

    role = models.PositiveSmallIntegerField(choices = ROLE_CHOICES)

    def __str__(self):
        return self.last_name + ", " + self.first_name