from django.contrib.auth import get_user_model
from django.db import models

class Point(models.Model):
    owner = models.ForeignKey(to=get_user_model(), related_name='point', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)


class PointTransaction(models.Model):
    amount = models.IntegerField()
    from_user = models.ForeignKey(to=get_user_model(), related_name='point', on_delete=models.CASCADE)
    to_user = models.ForeignKey(to=get_user_model(), related_name='point', on_delete=models.CASCADE)

    # transaction_type = models.
    transaction_at = models.DateTimeField()
