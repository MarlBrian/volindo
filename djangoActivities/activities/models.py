from django.db import models
from activities.user.models import User


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    participants = models.IntegerField()
    price = models.FloatField()
    link = models.URLField()
    key = models.BigIntegerField(unique=True)
    accessibility = models.FloatField
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} for user {self.user.name}"

