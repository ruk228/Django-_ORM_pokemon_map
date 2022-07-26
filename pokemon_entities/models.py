from email.base64mime import header_length
from django.db import models  # noqa F401
from django.forms.models import model_to_dict
from django.utils.timezone import localtime
# your models here

class Pokemon(models.Model):
    name = models.TextField(null=True, max_length=25, verbose_name='Русское имя')
    name_en = models.TextField(null=True, max_length=25, verbose_name='Английское имя')
    name_jp = models.TextField(null=True, max_length=25, verbose_name='Японское имя')
    image = models.ImageField(null=True, verbose_name='Название картинки')

    def __str__(self):
        return '{}'.format(self.name)


class PokemonEntity(models.Model):
    author = models.ForeignKey('Pokemon', null=True, verbose_name='Покемон', on_delete=models.CASCADE, related_name='pokemon')
    description = models.TextField(blank=True, verbose_name='Описание')
    lat = models.FloatField(blank=True, verbose_name='Широта')
    low = models.FloatField(null=True, verbose_name='Долгота')
    appeared_at = models.DateTimeField(blank=True, verbose_name='Время включения')
    disappeared_at = models.DateTimeField(blank=True, verbose_name='Время отключения')
    level = models.IntegerField(blank=True, verbose_name='Уровень')
    health = models.IntegerField(blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank=True, verbose_name='Прочность')
    defencer = models.IntegerField(blank=True, verbose_name='Защита')
    stamina = models.IntegerField(blank=True, verbose_name='стамина')

    def __str__(self):
        return '{}'.format(self.author)
