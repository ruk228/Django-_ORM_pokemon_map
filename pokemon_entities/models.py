from email.base64mime import header_length
from django.db import models  # noqa F401
from django.forms.models import model_to_dict
from django.utils.timezone import localtime
# your models here

class Pokemon(models.Model):
    name = models.TextField(max_length=25, blank=True)
    name_en = models.TextField(max_length=25, blank=True)
    name_jp = models.TextField(max_length=25, blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class PokemonEntity(models.Model):
    author = models.ForeignKey('Pokemon', verbose_name='Покемон', blank=True, on_delete=models.CASCADE, related_name='pokemon')
    description = models.TextField(null=True, verbose_name='Описание')
    lat = models.FloatField(null=True, verbose_name='Широта')
    low = models.FloatField(null=True, verbose_name='Долгота')
    appeared_at = models.DateTimeField(null=True, verbose_name='Время_включения')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Время_отключения')
    level = models.IntegerField(null=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, verbose_name='Прочность')
    defencer = models.IntegerField(null=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, verbose_name='стамина')

    def __str__(self):
        return '{}'.format(self.author)
