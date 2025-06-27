# Trip Weather API

A simple Flask API that provides weather forecasts and tourist attractions for a selected city using OpenWeatherMap and OpenStreetMap (Overpass API).

## Features
- Get weather forecast for any city (OpenWeatherMap)
- Get tourist attractions, historic sites, parks, and museums (OpenStreetMap/Overpass API)
- Filter attractions by radius (in km) from city center
- Data validation and formatting with Pydantic

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Setup
1. Clone the repository or copy the files.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenWeatherMap API key as an environment variable:
   ```bash
   set OPENWEATHER_API_KEY=your_api_key_here  # Windows
   export OPENWEATHER_API_KEY=your_api_key_here  # Linux/Mac
   ```
4. Run the app:
   ```bash
   python app.py
   ```

## Usage
- Home: [http://localhost:5000/](http://localhost:5000/)
- Example endpoint:
  - `/api/data/Zabrze` — all attractions in Zabrze
  - `/api/data/Zabrze?radius=10` — attractions within 10 km of Zabrze center

## Response Example
```json
{
  "city": "Zabrze",
  "weather": { ... },
  "attractions": [ ... ]
}
```

## Notes
- Attractions are filtered to include only those with a name.
- The API uses several OSM tags: `tourism=attraction`, `historic=*`, `leisure=park`, `amenity=museum`.
- The radius filter uses the city center coordinates from OpenWeatherMap.