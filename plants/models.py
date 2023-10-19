from django.db import models


# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=100)
    botanical_name = models.CharField(max_length=100, null=True)
    details = models.TextField(null=True)
    image = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name
