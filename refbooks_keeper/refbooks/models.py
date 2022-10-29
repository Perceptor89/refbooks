from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Refbook(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField()


class Version(models.Model):
    refbook = models.ForeignKey(Refbook, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['refbook', 'name'],
                name='unique_version'
            ),
            models.UniqueConstraint(
                fields=['refbook', 'start_date'],
                name='unique_start_date'
            )
        ]


class Element(models.Model):
    Version = models.ForeignKey(Version, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
