from django.db import models  # noqa F401
from django.forms.models import model_to_dict

# your models here

class Pokemon(models.Model):
    title = models.TextField(max_length=200, blank=True)
    #шаг 6 сделать!!! image = models.ImageField(null=True)

    def __str__(self):
        return '{}'.format(self.title)


class PokemonEntity(models.Model):
    # шаг 8 !!! author = models.ForeignKey(Pokemon, on_delete=models.SET_DEFAULT)
    lat = models.FloatField()
    low = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()