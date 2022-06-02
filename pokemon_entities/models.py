from django.db import models  # noqa F401

# your models here

class Pokemon(models.Model):
    title = models.TextField(max_length=200)
    #шаг 6 сделать!!! image = models.ImageField(null=True)

    def __str__(self):
        return '{}'.format(self.title)

class PokemonEntity(models.Model):
    lat = models.FloatField()
    low = models.FloatField()