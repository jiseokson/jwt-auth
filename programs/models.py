from django.db import models
from django.contrib.auth import get_user_model


class Program(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey(
        to=get_user_model(), related_name='program', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    start_at = models.DateTimeField(blank=False)
    end_at = models.DateTimeField(blank=False)

    subscriber = models.ManyToManyField(to=get_user_model())

    is_full = models.BooleanField(default=False)
    is_open = models.BooleanField(default=True)
    limit = models.IntegerField(default=0)

    # ...?
    compensation = models.IntegerField()

    # location = models...???
