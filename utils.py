from typing import Dict, Any
from models import WeatherEntry, WeatherResponse, Coord, Attraction, AttractionAddress, AttractionLinks

def parse_weather_response(data: Dict[str, Any]) -> Dict[str, Any]:
    city_info = data.get('city', {})
    coord = city_info.get('coord', {})
    weather_list = []
    for entry in data.get('list', []):
        main = entry.get('main', {})
        weather_desc = entry.get('weather', [{}])[0]
        
        weather_list.append(WeatherEntry(
            date = entry.get('dt_txt'),
            temp = main.get('temp'),
            temp_min = main.get('temp_min'),
            temp_max = main.get('temp_max'),
            pressure = main.get('pressure'),
            humidity = main.get('humidity'),
            wind_speed = entry.get('wind', {}).get('speed'),
            description = weather_desc.get('description')
        ))

    response = WeatherResponse(
        city_id = city_info.get('id'),
        city = city_info.get('name'),
        country = city_info.get('country'),
        coord = Coord(**coord),
        weather = weather_list
    )

    return response.dict()


def parse_attractions_response(data: dict) -> list:
    elements = data.get('elements', [])
    attractions = []
    for el in elements:
        tags = el.get('tags', {})
        if not tags.get('name'):
            continue
        
        address = AttractionAddress(
            city = tags.get('addr:city'),
            street = tags.get('addr:street'),
            housenumber = tags.get('addr:housenumber'),
            postcode = tags.get('addr:postcode'),
        ) if any(tags.get(f'addr:{k}') for k in ['city', 'street', 'housenumber', 'postcode']) else None
        
        links = AttractionLinks(
            website = tags.get('website'),
            image = tags.get('image'),
            url = tags.get('url'),
            wikipedia = tags.get('wikipedia'),
            wikidata = tags.get('wikidata'),
            other = {k: v for k, v in tags.items() if k.startswith('url:')}
        ) if any(tags.get(k) for k in ['website', 'image', 'url', 'wikipedia', 'wikidata']) or any(k.startswith('url:') for k in tags) else None
        
        attraction = Attraction(
            id = el.get('id'),
            name = tags.get('name'),
            address = address,
            links = links,
            lat = el.get('lat'),
            lon = el.get('lon'),
            type = el.get('type'),
        )
        
        attractions.append(attraction.dict())
    
    return attractions