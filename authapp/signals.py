from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, EmailOTPToken
from decouple import config
import requests
from django.conf import settings


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
    
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_email_user_token(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_superuser:
#             pass
#         EmailOTPToken.objects.create(user=instance)
#         otp = EmailOTPToken.objects.filter(user=instance).last().otp_code
#         url = "https://api.ng.termii.com/api/email/otp/send"
#         payload = {
#                     "api_key" : config("TERMII_API_KEY"),
#                     "email_address" : f"{instance.email}",
#                     "code": f"{otp}",
#                     "email_configuration_id": config("EMAIL_CONFIGURATION_ID")
#             }
#         headers = {
#         'Content-Type': 'application/json',
#         }
#         response = requests.request("POST", url, headers=headers, json=payload)