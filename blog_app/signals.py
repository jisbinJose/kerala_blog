from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Blogger

@receiver(post_save, sender=User)
def create_blogger_profile(sender, instance, created, **kwargs):
    if created:
        Blogger.objects.create(user=instance, bio="Welcome to my blog!")

@receiver(post_save, sender=User)
def save_blogger_profile(sender, instance, **kwargs):
    try:
        instance.blogger.save()
    except Blogger.DoesNotExist:
        Blogger.objects.create(user=instance, bio="Welcome to my blog!")
