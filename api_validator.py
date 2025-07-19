import asyncio
import aiohttp
import streamlit as st
from typing import Dict, Tuple, Optional
import requests
from openai import OpenAI
import time

class APIValidator:
    """Validates API credentials and connections"""
    
    def __init__(self):
        self.results = {}
    
    def test_openai_api(self, api_key: str) -> Tuple[bool, str]:
        """Test OpenAI API connection"""
        if not api_key or api_key.strip() == "":
            return False, "API key is empty"
        
        try:
            client = OpenAI(api_key=api_key)
            # Simple test call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True, "Connection successful"
        except Exception as e:
            error_msg = str(e)
            if "Invalid API key" in error_msg or "Incorrect API key" in error_msg:
                return False, "Invalid API key"
            elif "quota" in error_msg.lower():
                return False, "Quota exceeded"
            else:
                return False, f"Connection failed: {error_msg}"
    
    def test_google_places_api(self, api_key: str) -> Tuple[bool, str]:
        """Test Google Places API connection"""
        if not api_key or api_key.strip() == "":
            return False, "API key is empty"
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                'query': 'Marina Bay Singapore',
                'key': api_key
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK':
                    return True, "Connection successful"
                elif data.get('status') == 'REQUEST_DENIED':
                    return False, "API key invalid or service not enabled"
                else:
                    return False, f"API error: {data.get('status', 'Unknown')}"
            else:
                return False, f"HTTP error: {response.status_code}"
                
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def test_openweather_api(self, api_key: str) -> Tuple[bool, str]:
        """Test OpenWeather API connection"""
        if not api_key or api_key.strip() == "":
            return False, "API key is empty"
        
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': 1.3521,
                'lon': 103.8198,
                'appid': api_key,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return True, "Connection successful"
            elif response.status_code == 401:
                return False, "Invalid API key"
            else:
                return False, f"HTTP error: {response.status_code}"
                
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def test_all_apis(self, credentials: Dict[str, str]) -> Dict[str, Tuple[bool, str]]:
        """Test all APIs and return results"""
        results = {}
        
        # Test OpenAI
        if credentials.get('openai'):
            results['openai'] = self.test_openai_api(credentials['openai'])
        else:
            results['openai'] = (False, "No API key provided")
        
        # Test Google Places
        if credentials.get('google_places'):
            results['google_places'] = self.test_google_places_api(credentials['google_places'])
        else:
            results['google_places'] = (False, "No API key provided")
        
        # Test OpenWeather
        if credentials.get('openweather'):
            results['openweather'] = self.test_openweather_api(credentials['openweather'])
        else:
            results['openweather'] = (False, "No API key provided")
        
        return results
    
    def save_credentials_to_session(self, credentials: Dict[str, str]):
        """Save validated credentials to session state"""
        for key, value in credentials.items():
            st.session_state[f'api_{key}'] = value
        
        st.session_state['api_setup_complete'] = True
    
    def load_credentials_from_session(self) -> Dict[str, str]:
        """Load credentials from session state"""
        return {
            'openai': st.session_state.get('api_openai', ''),
            'google_places': st.session_state.get('api_google_places', ''),
            'openweather': st.session_state.get('api_openweather', '')
        }