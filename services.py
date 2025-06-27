import requests

def get_attractions(city, lat = None, lon = None, radius = None):
    if lat and lon and radius:
        query = f'''
        [out:json];
        (
          node["tourism"="attraction"](around:{radius},{lat},{lon});
          way["tourism"="attraction"](around:{radius},{lat},{lon});
          relation["tourism"="attraction"](around:{radius},{lat},{lon});
          node["historic"](around:{radius},{lat},{lon});
          way["historic"](around:{radius},{lat},{lon});
          relation["historic"](around:{radius},{lat},{lon});
          node["leisure"="park"](around:{radius},{lat},{lon});
          way["leisure"="park"](around:{radius},{lat},{lon});
          relation["leisure"="park"](around:{radius},{lat},{lon});
          node["amenity"="museum"](around:{radius},{lat},{lon});
          way["amenity"="museum"](around:{radius},{lat},{lon});
          relation["amenity"="museum"](around:{radius},{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        '''

    else:
        query = f'''
        [out:json];
        area["name"="{city}"]->.searchArea;
        (
          node["tourism"="attraction"](area.searchArea);
          way["tourism"="attraction"](area.searchArea);
          relation["tourism"="attraction"](area.searchArea);
          node["historic"](area.searchArea);
          way["historic"](area.searchArea);
          relation["historic"](area.searchArea);
          node["leisure"="park"](area.searchArea);
          way["leisure"="park"](area.searchArea);
          relation["leisure"="park"](area.searchArea);
          node["amenity"="museum"](area.searchArea);
          way["amenity"="museum"](area.searchArea);
          relation["amenity"="museum"](area.searchArea);
        );
        out body;
        >;
        out skel qt;
        '''

    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data = {"data": query})

    return response.json()


def get_weather(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    return response.json()