from allauth.account.signals import email_confirmed
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    contact_no = models.CharField(max_length=12)
    locality = models.CharField(max_length=255)


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.is_verified = True
    user.save()
