from typing import List, Optional, Dict
from pydantic import BaseModel

class Coord(BaseModel):
    lat: float
    lon: float

class WeatherEntry(BaseModel):
    date: str
    temp: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    wind_speed: Optional[float]
    description: str

class WeatherResponse(BaseModel):
    city_id: int
    city: str
    country: str
    coord: Coord
    weather: List[WeatherEntry]

class AttractionAddress(BaseModel):
    city: Optional[str]
    street: Optional[str]
    housenumber: Optional[str]
    postcode: Optional[str]

class AttractionLinks(BaseModel):
    website: Optional[str]
    image: Optional[str]
    url: Optional[str]
    wikipedia: Optional[str]
    wikidata: Optional[str]
    other: Optional[Dict[str, str]] = None

class Attraction(BaseModel):
    id: int
    name: Optional[str]
    address: Optional[AttractionAddress]
    links: Optional[AttractionLinks]
    lat: Optional[float]
    lon: Optional[float]
    type: str