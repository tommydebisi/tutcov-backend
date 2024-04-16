# myapp/models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import uuid
from .managers import UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
import random
import string

class Department(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name




class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True) # I  removed the default
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    level = models.CharField(max_length=50, blank=True)
    faculty = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='tutdb_users_groups',  # Specify a custom related name
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user-permissions'),
        blank=True,
        related_name='tutdb_users_permissions',  # Specify a custom related name
        help_text=_('Specific permissions for this user.'),
    )

    def has_perm(self, perm, obj=None):
        """
        Check if the user has a specific permission.

        Args:
            perm (str): The codename of the permission to check.
            obj (object, optional): An optional object for checking object-specific permissions.
                Defaults to None when checking global permissions.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        if self.is_active and self.is_staff:
            # Staff members have all permissions
            return True
        else:
            try:
                # Attempt to retrieve the permission from user_permissions
                user_perm = self.user_permissions.get(codename=perm)
            except ObjectDoesNotExist:
                # Permission not found in user_permissions
                user_perm = False

            if user_perm:
                # User has the permission
                return True
            else:
                # User does not have the permission
                return False

    class Meta:
        permissions = (
            ("support_view", "can view pqs"),
            ("support_edit", "can edit pqs"),
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']  # Add 'password' to the REQUIRED_FIELDS list

    def __str__(self):
        return self.email


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token_expires_at = models.DateTimeField()
    refresh_token_expires_at = models.DateTimeField()


    def save(self, *args, **kwargs):
        if not self.id:
            # If the instance is being created (not updated), set expired_at to 30 minutes from now.
            self.access_token_expires_at = timezone.now() + timedelta(minutes=30)
            self.refresh_token_expires_at = timezone.now() + timedelta(hours=12)
        super(Token, self).save(*args, **kwargs)

    def is_access_token_expired(self):
        return timezone.now() >= self.access_token_expires_at

    def is_refresh_token_expired(self):
        return timezone.now() >= self.refresh_token_expires_at
    



class Question(models.Model):
    question = models.CharField(max_length=255)
    image = models.ImageField(upload_to="question_images", blank=True, null=True)
    OPTION_CHOICES = (
        ('Option 1', 'Option 1'),
        ('Option 2', 'Option 2'),
        ('Option 3', 'Option 3'),
        ('Option 4', 'Option 4'),
    )
    options = models.CharField(max_length=50, choices=OPTION_CHOICES)
    picked_answer = models.CharField(max_length=1, blank=True)
    answer = models.CharField(max_length=1)
    question_number = models.IntegerField()

    def __str__(self):
        return self.question
