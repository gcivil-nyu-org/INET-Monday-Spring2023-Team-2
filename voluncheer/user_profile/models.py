from django.db import models
from datetime import datetime
import random

# Create your models here.

# ===================== Global Variables ===========================
GLOBAL_BADGES = {
    "Badge 1": "images/badge-1.png",
    "Badge 2": "images/badge-2.png",
    "Badge 3": "images/badge-3.png",
    "Badge 4": "images/badge-4.png",
    "Badge 5": "images/badge-5.png",
    "Badge 6": "images/badge-6.png",
}
class User(models.Model):
    user_name = models.CharField(max_length=256)
    user_email = models.CharField(max_length=256)
    user_address_city = models.CharField(max_length=256)
    user_address_zipcode = models.IntegerField()
    user_skill = models.CharField(max_length=1024, default="") # program,sing,dance
    user_badges = models.CharField(max_length=1024, default="") # 0,1,2
    user_preference = models.CharField(max_length=1024, default="") # adventurous,full-time
    user_image = models.CharField(max_length=256)