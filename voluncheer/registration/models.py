from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLE_CHOICES = (
    ('volunteer', 'Volunteer'),
    ('organization','Organization'),
)

class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    date_of_birth = models.DateField(blank = True, null = True) 
    email = models.EmailField(max_length = 254, unique = True)
    password = models.CharField(max_length = 127)
    role = models.CharField(max_length = 12, choices = ROLE_CHOICES, default = 'volunteer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [role]

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.last_name + ", " + self.first_name