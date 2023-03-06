from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Volunteer

User = get_user_model()

@receiver(post_save, sender=User)
def volunteer_signup(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, 'volunteer'):
            Volunteer.objects.create(user=instance)