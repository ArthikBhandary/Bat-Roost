from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.signals import email_confirmed
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)



@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.is_verified = True
    user.save()
