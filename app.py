from flask import Flask, request, jsonify
import os
from requests.exceptions import RequestException

from services import get_attractions, get_weather
from utils import parse_weather_response, parse_attractions_response

app = Flask(__name__)

@app.route('/')
def home():
    return (
        '<h2>Trip Weather API</h2>'
        '<p>Use the endpoint <code>/api/data/&lt;city&gt;?radius=&lt;km&gt;</code> to get weather forecast and tourist attractions for a selected city.</p>'
        '<p>Example: <code>/api/data/Katowice?radius=10</code></p>'
    )

@app.route('/api/data/<city>')
def api_data(city: str):
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
        
    weather_api_key = os.environ.get('OPENWEATHER_API_KEY')
    
    try:
        weather_raw = get_weather(city, weather_api_key)
    except RequestException:
        return jsonify({'error': 'Weather API connection error'}), 502
    
    if not weather_raw or 'city' not in weather_raw:
        return jsonify({'error': 'No weather data for this city'}), 404
    
    try:
        weather = parse_weather_response(weather_raw)
    except Exception:
        return jsonify({'error': 'Weather data parsing error'}), 500
    
    coord = weather.get('coord', {})
    lat = coord.get('lat')
    lon = coord.get('lon')
    radius_km = request.args.get('radius')
    
    try:
        if radius_km is not None and radius_km.isdigit():
            radius = int(radius_km) * 1000
            raw_attractions = get_attractions(city, lat = lat, lon = lon, radius = radius)
        else:
            raw_attractions = get_attractions(city)
    except RequestException:
        return jsonify({'error': 'Attractions API connection error'}), 502
    except Exception:
        return jsonify({'error': 'Attractions data error'}), 500
    
    if not raw_attractions or 'elements' not in raw_attractions:
        return jsonify({'error': 'No attractions data for this city'}), 404
    
    try:
        attractions = parse_attractions_response(raw_attractions)
    except Exception:
        return jsonify({'error': 'Attractions data parsing error'}), 500

    return jsonify({
        'city': city,
        'weather': weather,
        'attractions': attractions
    })

if __name__ == '__main__':
    app.run(debug = True)