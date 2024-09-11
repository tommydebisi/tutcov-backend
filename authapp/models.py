# myapp/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
import random
import string
from django.utils.text import slugify
from django.conf import settings
import secrets

class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Faculty(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# YEAR = (
#     ("100 Level", "100 Level"),
#     ("200 Level", "200 Level"),
#     ("300 Level", "300 Level"),
#     ("400 Level", "400 Level"),
#     ("500 Level", "500 Level")
# )

# FACULTY_CHOICES = (
#     ("Engineering", "Engineering"),
# )

# DEPARTMENT_CHOICES = (
#     ("Computer Engineering", "Computer Engineering"),
#     ("Electrical Engineering", "Electrical Engineering")
# )


# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=30, unique=True) # I  removed the default
#     image = models.ImageField(default="user.jpg", upload_to="profile_pictures")
#     level = models.CharField(max_length=50, choices=YEAR)
#     country = models.CharField(max_length=100, default="Nigeria")
#     faculty = models.CharField(choices=FACULTY_CHOICES, max_length=255)
#     phone_number = models.CharField(max_length=11)
#     department = models.CharField(choices=DEPARTMENT_CHOICES, max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_lecturer = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)

#     objects = UserManager()

#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name=_('groups'),
#         blank=True,
#         related_name='tutdb_users_groups',  # Specify a custom related name
#         help_text=_(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name=_('user-permissions'),
#         blank=True,
#         related_name='tutdb_users_permissions',  # Specify a custom related name
#         help_text=_('Specific permissions for this user.'),
#     )

#     def has_perm(self, perm, obj=None):
#         """
#         Check if the user has a specific permission.

#         Args:
#             perm (str): The codename of the permission to check.
#             obj (object, optional): An optional object for checking object-specific permissions.
#                 Defaults to None when checking global permissions.

#         Returns:
#             bool: True if the user has the permission, False otherwise.
#         """
#         if self.is_active and self.is_staff:
#             # Staff members have all permissions
#             return True
#         else:
#             try:
#                 # Attempt to retrieve the permission from user_permissions
#                 user_perm = self.user_permissions.get(codename=perm)
#             except ObjectDoesNotExist:
#                 # Permission not found in user_permissions
#                 user_perm = False

#             if user_perm:
#                 # User has the permission
#                 return True
#             else:
#                 # User does not have the permission
#                 return False

#     class Meta:
#         permissions = (
#             ("support_view", "can view pqs"),
#             ("support_edit", "can edit pqs"),
#         )

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username', 'password']  # Add 'password' to the REQUIRED_FIELDS list

#     def __str__(self):
#         return self.email


# class Token(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     access_token = models.CharField(max_length=255)
#     refresh_token = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     access_token_expires_at = models.DateTimeField()
#     refresh_token_expires_at = models.DateTimeField()


#     def save(self, *args, **kwargs):
#         if not self.id:
#             # If the instance is being created (not updated), set expired_at to 30 minutes from now.
#             self.access_token_expires_at = timezone.now() + timedelta(minutes=30)
#             self.refresh_token_expires_at = timezone.now() + timedelta(hours=12)
#         super(Token, self).save(*args, **kwargs)

#     def is_access_token_expired(self):
#         return timezone.now() >= self.access_token_expires_at

#     def is_refresh_token_expired(self):
#         return timezone.now() >= self.refresh_token_expires_at


# YEAR = (
#     ("100 Level", "100 Level"),
#     ("200 Level", "200 Level"),
#     ("300 Level", "300 Level"),
#     ("400 Level", "400 Level"),
#     ("500 Level", "500 Level")
# )




# class EmailOTPToken(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_otps")
#     otp_code = models.CharField(max_length=4)
#     otp_created_at = models.DateTimeField(auto_now_add=True)
#     otp_expires_at = models.DateTimeField()

#     def __str__(self):
#         return self.user.email
    
#     def save(self, *args, **kwargs):
#         if not self.otp_expires_at:
#             self.otp_expires_at = timezone.now() + timedelta(minutes=5)
#         if not self.otp_code:
#             self.otp_code = '{:04d}'.format(secrets.randbelow(10000))
            
#         super(EmailOTPToken, self).save(*args, **kwargs)

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     image = models.ImageField(default="user.jpg", upload_to="profile_pictures")
#     full_name = models.CharField(max_length=200, blank=True, null=True)
    

#     def __str__(self):
#         return f"{self.user.username} Profile"