from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __repr__(self):
        return f"User {self.name}, id {self.id}"

    def __str__(self):
        return repr(self)