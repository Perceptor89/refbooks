from django.db import models


class Refbook(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    owner = models.ForeignKey(
        'auth.User',
        related_name='refbooks',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Version(models.Model):
    refbook = models.ForeignKey(Refbook, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_date = models.DateField()

    def __str__(self):
        return self.name

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
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=300)

    def __str__(self):
        return self.code
