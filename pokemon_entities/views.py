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


def get_information_pokemons(request, pokemon_id=True):
    entities = []
    pokemons_info = []
    pokemons_entity = PokemonEntity.objects.filter(disappeared_at__gte=localtime(), appeared_at__lte=localtime())

    for pokemon_entity in pokemons_entity:

        #nex_pokemon_entity = PokemonEntity.objects.filter(isappeared_at__gte=localtime(), appeared_at__lte=localtime())
        #print(nex_pokemon_entity)
        next_evolution = {
                    "title_ru": pokemon_entity.author.name,
                    "pokemon_id": pokemon_entity.id,
                    "img_url": request.build_absolute_uri('media/{}'.format(pokemon_entity.author.image))
                }
        previous_evolution = {
                    "title_ru": "Бульбазавр",
                    "pokemon_id": 1,
                    "img_url": "https://upload.wikimedia.org/wikipedia/ru/c/ca/%D0%91%D1%83%D0%BB%D1%8C%D0%B1%D0%B0%D0%B7%D0%B0%D0%B2%D1%80.png"
                }
        entities = {
            'lat': pokemon_entity.lat,
            'level': pokemon_entity.level,
            'lon': pokemon_entity.low
        }
        pokemons_info.append(
            {
                "pokemon_id": pokemon_id,
                "title_ru": pokemon_entity.author.name,
                "title_en": pokemon_entity.author.name_en,
                "title_jp": pokemon_entity.author.name_jp,
                "description": pokemon_entity.description,
                "img_url": request.build_absolute_uri('media/{}'.format(pokemon_entity.author.image)),
                "entities": entities,
                "next_evolution": next_evolution,
                "previous_evolution": previous_evolution
            }
        )
    return pokemons_info


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)    
    pokemons_on_page = []
    pokemons_entity = PokemonEntity.objects.filter(disappeared_at__gte=localtime(), appeared_at__lte=localtime())

    for pokemon_entity in pokemons_entity:
        img_url = request.build_absolute_uri('media/{}'.format(pokemon_entity.author.image))

        pokemons_on_page.append({
            'pokemon_id':  pokemon_entity.id,
            'img_url': img_url,
            'title_ru': pokemon_entity.author.name
        })

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.low,
            img_url
        )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = []
    pokemon_id = int(pokemon_id)
    pokemons_entity = PokemonEntity.objects.filter(disappeared_at__gte=localtime(), appeared_at__lte=localtime())
    pokemon_entity = pokemons_entity[pokemon_id-1]

    try:
        previous_pokemon_entity = Pokemon.objects.get(id=pokemon_id)
        previous_evolution = {
            "title_ru": previous_pokemon_entity.name,
            "pokemon_id": previous_pokemon_entity.id,
            "img_url": request.build_absolute_uri('../../media/{}'.format(previous_pokemon_entity.image))#проблемаа с  author
        }
    except:
        previous_evolution = {}

    try:
        next_pokemon_entity = pokemons_entity[pokemon_id]
        next_evolution = {
            "title_ru": next_pokemon_entity.author.name,
            "pokemon_id": next_pokemon_entity.id,
            "img_url": request.build_absolute_uri('../../media/{}'.format(next_pokemon_entity.author.image))
        }
    except:
        next_evolution = {}

    pokemons.append(
        {
        'pokemon_id': pokemon_entity.id,
        'title_ru': pokemon_entity.author.name,
        'title_en': pokemon_entity.author.name_en,
        'title_jp': pokemon_entity.author.name_jp,
        'description': pokemon_entity.description,
        'img_url': request.build_absolute_uri('../../media/{}'.format(pokemon_entity.author.image)),
        'entities': [#исправить(добавить append параметрво покемонов если хи больше 1-го)
            {
            'level': pokemon_entity.level,
            'lat': pokemon_entity.lat,
            'lon': pokemon_entity.low
            },
            {
            'level': pokemon_entity.level,
            'lat': pokemon_entity.lat,
            'lon': pokemon_entity.low
            }
            ],
        "next_evolution": next_evolution,
        'previous_evolution': previous_evolution
        },
    )


    for pokemon in pokemons:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon['entities']:
        add_pokemon(
            folium_map, pokemon_entity['lat'],
            pokemon_entity['lon'],
            pokemon['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })

