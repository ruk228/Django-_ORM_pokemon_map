import folium
import json

from .models import PokemonEntity, Pokemon
from django.http import HttpResponseNotFound
from django.shortcuts import render
from requests import request
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)

    
def get_information_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemons_info = []

    for pokemon in pokemons:
        pokemon_entity = PokemonEntity.objects.filter(disappeared_at__gte=localtime(), appeared_at__lte=localtime(), author__name='Бульбазавр').first()

        pokemons_info.append({
            'description': pokemon_entity.description,
            'entities': [{
                'lat': pokemon_entity.lat,
                'level': pokemon_entity.level,
                'lon': pokemon_entity.low
            }],
            'img_url': request.build_absolute_uri('media/{}'.format(pokemon.image)),
            'next_evolution': {
                'img_url': request.build_absolute_uri('media/{}'.format(pokemon.image)),#rубрать копипаст ссылки
                'pokemon_id': pokemon_entity.author.id+1,
                'title_ru': 'Ивизавр'
            },
            'pokemon_id': pokemon_entity.author.id,
            'title_en': pokemon.name_en,
            'title_jp': pokemon.name_jp,
            'title_ru': pokemon.name
        })

    return pokemons_info


def show_all_pokemons(request):
    pokemons_info = get_information_pokemons(request)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)    
    pokemons_on_page = []

    for pokemon in pokemons_info:#переименовать
        pokemons_on_page.append({
            'pokemon_id': pokemon['pokemon_id'],
            'img_url': pokemon['img_url'],
            'title_ru': pokemon['title_ru'],
        })

        for pokemon_entity in pokemon['entities']:
            add_pokemon(
                folium_map, pokemon_entity['lat'],
                pokemon_entity['lon'],
                pokemon['img_url']
            )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons_info = get_information_pokemons(request)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons_info:#переименовать
        for pokemon_entity in pokemon['entities']:
            add_pokemon(
                folium_map, pokemon_entity['lat'],
                pokemon_entity['lon'],
                pokemon['img_url']
            )

    for pokemon in pokemons_info:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
