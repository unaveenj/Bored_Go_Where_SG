import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration management for API keys and settings"""
    
    @staticmethod
    def get_openai_key():
        """Get OpenAI API key from environment or Streamlit secrets"""
        try:
            return (
                os.getenv("OPENAI_API_KEY") or 
                st.secrets.get("OPENAI_API_KEY", "")
            )
        except:
            return os.getenv("OPENAI_API_KEY", "")
    
    @staticmethod
    def get_mapbox_token():
        """Get Mapbox access token from environment or Streamlit secrets"""
        try:
            return (
                os.getenv("MAPBOX_ACCESS_TOKEN") or 
                st.secrets.get("MAPBOX_ACCESS_TOKEN", "")
            )
        except:
            return os.getenv("MAPBOX_ACCESS_TOKEN", "")
    
    @staticmethod
    def get_google_places_key():
        """Get Google Places API key from environment or Streamlit secrets"""
        try:
            return (
                os.getenv("GOOGLE_PLACES_API_KEY") or 
                st.secrets.get("GOOGLE_PLACES_API_KEY", "")
            )
        except:
            return os.getenv("GOOGLE_PLACES_API_KEY", "")
    
    @staticmethod
    def get_openweather_key():
        """Get OpenWeather API key from environment or Streamlit secrets"""
        try:
            return (
                os.getenv("OPENWEATHER_API_KEY") or 
                st.secrets.get("OPENWEATHER_API_KEY", "")
            )
        except:
            return os.getenv("OPENWEATHER_API_KEY", "")
    
    @staticmethod
    def validate_keys():
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not Config.get_openai_key():
            missing_keys.append("OPENAI_API_KEY")
        if not Config.get_mapbox_token():
            missing_keys.append("MAPBOX_ACCESS_TOKEN")
        if not Config.get_google_places_key():
            missing_keys.append("GOOGLE_PLACES_API_KEY")
        if not Config.get_openweather_key():
            missing_keys.append("OPENWEATHER_API_KEY")
            
        return missing_keys

# App settings
SINGAPORE_CENTER = {"lat": 1.3521, "lon": 103.8198}
DEFAULT_ZOOM = 11
BUY_ME_COFFEE_URL = "https://www.buymeacoffee.com/yourusername"