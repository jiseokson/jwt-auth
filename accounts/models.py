import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import OAUTH_PROVIDER_CHOICES, CustomUserManager, OAuthUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_register = models.BooleanField(
        _('register'),
        default=False,
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    oauth_id = models.CharField(
        _('oauth id'),
        max_length=128,
        default=None,
        null=True, blank=True
    )
    oauth_provider = models.CharField(
        _('oauth provider'),
        max_length=100,
        choices=OAUTH_PROVIDER_CHOICES,
        default=None,
        null=True, blank=True,
    )

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()
    oauths = OAuthUserManager()

    def __str__(self):
        return self.username
