from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager, DefaultAuthUserManafer, OAuthUserManager

OAUTH_PROVIDER = [
    'google',
    'kakao',
    'github',
]

OAUTH_PROVIDER_CHOICES = [(provider, provider) for provider in OAUTH_PROVIDER]

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("email"), unique=True)
    first_name = models.CharField('first name', max_length=100)
    last_name = models.CharField('last name', max_length=100)

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
    oauth_auths = OAuthUserManager()
    default_auths = DefaultAuthUserManafer()

    def __str__(self):
        return self.email