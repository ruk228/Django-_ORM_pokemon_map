from django.db import models  # noqa F401

# your models here
class Pokemon(models.Model):
    title = models.TextField(max_length=200, blank=True)

