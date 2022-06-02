from django.contrib import admin

import pokemon_entities
from .models import Pokemon

admin.site.register(Pokemon)