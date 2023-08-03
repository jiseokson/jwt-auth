from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models


class Program(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(
        to=get_user_model(), related_name='author', on_delete=models.CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    regist_start_at = models.DateTimeField()
    regist_end_at = models.DateTimeField()

    activity_start_at = models.DateTimeField()
    activity_end_at = models.DateTimeField()

    is_registing = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    subscriber_limit = models.IntegerField()
    subscriber = models.ManyToManyField(
        to=get_user_model(), related_name='program')

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
