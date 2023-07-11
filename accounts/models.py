from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import OAUTH_PROVIDER_CHOICES, CustomUserManager, DefaultAuthUserManager, OAuthUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)

    oauth_provider = models.CharField(
        max_length=100,
        choices=OAUTH_PROVIDER_CHOICES,
        default=None,
        null=True, blank=True,
    )
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    oauths = OAuthUserManager()
    default_auths = DefaultAuthUserManager()

    def __str__(self):
        return self.email