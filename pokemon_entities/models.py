from email.base64mime import header_length
from django.db import models  # noqa F401
from django.forms.models import model_to_dict
from django.utils.timezone import localtime
# your models here

class Pokemon(models.Model):
    name = models.TextField(max_length=200, blank=True)#blank=True убрать
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class PokemonEntity(models.Model):
    author = models.ForeignKey(Pokemon, null=True, on_delete=models.CASCADE)#null=True убрать
    description = models.TextField(null=True)
    lat = models.FloatField(null=True)
    low = models.FloatField(null=True)
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    strength = models.IntegerField(null=True)
    defencer = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)
