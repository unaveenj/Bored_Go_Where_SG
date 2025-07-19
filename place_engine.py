import requests
import json
import streamlit as st
from typing import List, Dict, Optional
from config import Config, SINGAPORE_CENTER

class PlaceSuggestionEngine:
    """Engine for suggesting places based on user preferences"""
    
    def __init__(self):
        # Try session state first (from API setup page), then fallback to config
        self.google_api_key = st.session_state.get('api_google_places') or Config.get_google_places_key()
        self.openweather_key = st.session_state.get('api_openweather') or Config.get_openweather_key()
        
    def search_places(self, query: str, location: Dict = None, radius: int = 5000, 
                     place_type: str = None, price_level: List[int] = None) -> List[Dict]:
        """Search for places using Google Places API"""
        if not self.google_api_key:
            return self._get_fallback_places()
            
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        if not location:
            location = SINGAPORE_CENTER
            
        params = {
            'query': query,
            'location': f"{location['lat']},{location['lon']}",
            'radius': radius,
            'key': self.google_api_key
        }
        
        if place_type:
            params['type'] = place_type
            
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            places = []
            for place in data.get('results', [])[:10]:  # Limit to 10 results
                place_info = {
                    'name': place.get('name', 'Unknown'),
                    'address': place.get('formatted_address', 'Address not available'),
                    'rating': place.get('rating', 0),
                    'price_level': place.get('price_level', 0),
                    'types': place.get('types', []),
                    'lat': place['geometry']['location']['lat'],
                    'lng': place['geometry']['location']['lng'],
                    'place_id': place.get('place_id', ''),
                    'photo_reference': self._get_photo_reference(place)
                }
                
                # Filter by price level if specified
                if price_level and place_info['price_level'] not in price_level:
                    continue
                    
                places.append(place_info)
                
            return places
            
        except Exception as e:
            print(f"Error searching places: {e}")
            return self._get_fallback_places()
    
    def _get_photo_reference(self, place: Dict) -> Optional[str]:
        """Extract photo reference from place data"""
        photos = place.get('photos', [])
        if photos:
            return photos[0].get('photo_reference')
        return None
    
    def get_weather(self, lat: float, lon: float) -> Dict:
        """Get current weather for a location"""
        if not self.openweather_key:
            return {'condition': 'Unknown', 'temp': 0, 'description': 'Weather data unavailable'}
            
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.openweather_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            return {
                'condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'rain': 'rain' in data
            }
        except Exception as e:
            print(f"Error getting weather: {e}")
            return {'condition': 'Unknown', 'temp': 0, 'description': 'Weather data unavailable'}
    
    def filter_by_mood(self, places: List[Dict], mood: str) -> List[Dict]:
        """Filter places based on user mood"""
        mood_filters = {
            'chill': ['cafe', 'park', 'library', 'spa', 'bookstore'],
            'active': ['gym', 'sports', 'hiking', 'adventure', 'outdoor'],
            'romantic': ['restaurant', 'rooftop', 'garden', 'sunset', 'fine_dining'],
            'cultural': ['museum', 'gallery', 'theater', 'heritage', 'temple'],
            'random': []  # No filter for random
        }
        
        if mood == 'random' or mood not in mood_filters:
            return places
            
        keywords = mood_filters[mood]
        filtered = []
        
        for place in places:
            place_types = [t.lower() for t in place.get('types', [])]
            place_name = place.get('name', '').lower()
            
            if any(keyword in ' '.join(place_types + [place_name]) for keyword in keywords):
                filtered.append(place)
                
        return filtered if filtered else places[:3]  # Return first 3 if no matches
    
    def filter_by_budget(self, places: List[Dict], budget: str) -> List[Dict]:
        """Filter places based on budget"""
        budget_map = {
            'free': [0],
            'cheap': [0, 1],
            'moderate': [1, 2],
            'splurge': [3, 4]
        }
        
        if budget not in budget_map:
            return places
            
        allowed_levels = budget_map[budget]
        return [p for p in places if p.get('price_level', 0) in allowed_levels]
    
    def _get_fallback_places(self) -> List[Dict]:
        """Fallback places when API is unavailable"""
        return [
            {
                'name': 'Marina Bay Sands',
                'address': '10 Bayfront Ave, Singapore 018956',
                'rating': 4.3,
                'price_level': 3,
                'types': ['tourist_attraction', 'shopping_mall'],
                'lat': 1.2834,
                'lng': 103.8607,
                'place_id': 'fallback_1',
                'photo_reference': None
            },
            {
                'name': 'Gardens by the Bay',
                'address': '18 Marina Gardens Dr, Singapore 018953',
                'rating': 4.5,
                'price_level': 2,
                'types': ['park', 'tourist_attraction'],
                'lat': 1.2816,
                'lng': 103.8636,
                'place_id': 'fallback_2',
                'photo_reference': None
            },
            {
                'name': 'Orchard Road',
                'address': 'Orchard Rd, Singapore',
                'rating': 4.2,
                'price_level': 2,
                'types': ['shopping_mall', 'tourist_attraction'],
                'lat': 1.3048,
                'lng': 103.8318,
                'place_id': 'fallback_3',
                'photo_reference': None
            }
        ]