# myapp/models.py
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, default="None")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    level = models.CharField(max_length=50, blank=True)
    faculty = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
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
    REQUIRED_FIELDS = ['password']  # Add 'password' to the REQUIRED_FIELDS list

    def __str__(self):
        return self.email


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    access_token_expires_at = models.DateTimeField()
    refresh_token_expires_at = models.DateTimeField()

    def is_access_token_expired(self):
        return timezone.now() >= self.access_token_expires_at

    def is_refresh_token_expired(self):
        return timezone.now() >= self.refresh_token_expires_at
