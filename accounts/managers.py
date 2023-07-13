from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

OAUTH_PROVIDER = [
    'google',
    'kakao',
    'github',
]

OAUTH_PROVIDER_CHOICES = [(provider, provider) for provider in OAUTH_PROVIDER]

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        return self.create_user(username, password, **extra_fields)

class OAuthUserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(oauth_provider__in=OAUTH_PROVIDER)
    
    def create_user(self, oauth_provider, oauth_id, **extra_fields):
        if not oauth_id:
            raise ValueError(_("The ID must be set"))
        if not oauth_provider:
            raise ValueError(_("The OAuth provider must be set"))
        
        user = self.model(
            username=(oauth_id + '@' + oauth_provider),
            oauth_id=oauth_id,
            oauth_provider=oauth_provider,
            **extra_fields
        )
        user.set_unusable_password()
        user.save()
        return user