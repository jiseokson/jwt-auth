from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models


class Program(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        to=get_user_model(), related_name='author', on_delete=models.CASCADE)
    content = models.TextField()

    subscriber_count_limit = models.IntegerField(default=0)
    subscriber = models.ManyToManyField(
        to=get_user_model(), related_name='subscribed')

    is_active = models.BooleanField(default=True)
    is_full = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
