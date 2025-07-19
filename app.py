import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
from typing import List, Dict
import re
from openai import OpenAI

from config import Config, SINGAPORE_CENTER, BUY_ME_COFFEE_URL
from place_engine import PlaceSuggestionEngine

# Page configuration
st.set_page_config(
    page_title="Bored Go Where SG",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 3em;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 2em;
    }
    .place-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .coffee-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

class BoredGoWhereApp:
    def __init__(self):
        self.engine = PlaceSuggestionEngine()
        self.openai_client = self._init_openai()
        
    def _init_openai(self):
        """Initialize OpenAI client"""
        api_key = Config.get_openai_key()
        if api_key:
            return OpenAI(api_key=api_key)
        return None
    
    def parse_user_intent(self, user_input: str) -> Dict:
        """Parse user input to extract intent and preferences"""
        intent = {
            'query': user_input.lower(),
            'mood': 'random',
            'budget': 'moderate',
            'time_of_day': 'any',
            'location_preference': None
        }
        
        # Simple pattern matching for demo
        mood_patterns = {
            'chill': ['chill', 'relax', 'calm', 'peaceful', 'quiet'],
            'active': ['active', 'sport', 'exercise', 'adventure', 'outdoor'],
            'romantic': ['romantic', 'date', 'couple', 'intimate'],
            'cultural': ['cultural', 'museum', 'art', 'heritage', 'history']
        }
        
        budget_patterns = {
            'free': ['free', 'no cost', 'budget', 'cheap'],
            'splurge': ['expensive', 'luxury', 'high-end', 'splurge']
        }
        
        # Extract mood
        for mood, keywords in mood_patterns.items():
            if any(keyword in intent['query'] for keyword in keywords):
                intent['mood'] = mood
                break
                
        # Extract budget
        for budget, keywords in budget_patterns.items():
            if any(keyword in intent['query'] for keyword in keywords):
                intent['budget'] = budget
                break
                
        return intent
    
    def generate_ai_response(self, places: List[Dict], user_input: str) -> str:
        """Generate conversational response using OpenAI"""
        if not self.openai_client or not places:
            return self._generate_fallback_response(places, user_input)
            
        try:
            place_names = [p['name'] for p in places[:3]]
            prompt = f"""
            User said: "{user_input}"
            
            I found these places in Singapore: {', '.join(place_names)}
            
            Generate a friendly, conversational response (2-3 sentences) that:
            1. Acknowledges their boredom/request
            2. Introduces the suggestions enthusiastically
            3. Mentions why these places might be good for them
            
            Keep it casual and helpful, like a local friend giving advice.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"AI response error: {e}")
            return self._generate_fallback_response(places, user_input)
    
    def _generate_fallback_response(self, places: List[Dict], user_input: str) -> str:
        """Fallback response when AI is unavailable"""
        if not places:
            return "I couldn't find any specific places right now, but Singapore has so much to offer! Try being more specific about what you're in the mood for."
            
        place_count = len(places)
        return f"Found {place_count} interesting places for you! Here are some great options to cure your boredom in Singapore. Each has something unique to offer!"
    
    def create_map(self, places: List[Dict]) -> folium.Map:
        """Create Folium map with place markers"""
        m = folium.Map(
            location=[SINGAPORE_CENTER['lat'], SINGAPORE_CENTER['lon']],
            zoom_start=11,
            tiles='OpenStreetMap'
        )
        
        for i, place in enumerate(places[:10]):  # Limit to 10 markers
            popup_html = f"""
            <div style="width: 200px;">
                <h4>{place['name']}</h4>
                <p><strong>Rating:</strong> ⭐ {place['rating']}/5</p>
                <p><strong>Address:</strong> {place['address']}</p>
                <p><strong>Types:</strong> {', '.join(place['types'][:3])}</p>
            </div>
            """
            
            folium.Marker(
                location=[place['lat'], place['lng']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{i+1}. {place['name']}",
                icon=folium.Icon(color='red', icon=f'{i+1}', prefix='fa')
            ).add_to(m)
            
        return m
    
    def display_place_cards(self, places: List[Dict]):
        """Display place information as cards"""
        for i, place in enumerate(places):
            with st.container():
                st.markdown(f"""
                <div class="place-card">
                    <h3>#{i+1} {place['name']}</h3>
                    <p><strong>📍 Address:</strong> {place['address']}</p>
                    <p><strong>⭐ Rating:</strong> {place['rating']}/5</p>
                    <p><strong>💰 Price Level:</strong> {'$' * max(1, place['price_level'])}</p>
                    <p><strong>🏷️ Category:</strong> {', '.join(place['types'][:3])}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add weather info
                weather = self.engine.get_weather(place['lat'], place['lng'])
                if weather['condition'] != 'Unknown':
                    st.info(f"🌤️ Weather: {weather['description'].title()}, {weather['temp']:.0f}°C")
    
    def sidebar_filters(self) -> Dict:
        """Create sidebar with filters"""
        st.sidebar.title("🎛️ Filters")
        
        filters = {}
        
        filters['mood'] = st.sidebar.selectbox(
            "What's your mood?",
            ['random', 'chill', 'active', 'romantic', 'cultural'],
            help="Filter places based on your current mood"
        )
        
        filters['budget'] = st.sidebar.selectbox(
            "Budget preference:",
            ['moderate', 'free', 'cheap', 'splurge'],
            help="Filter by price range"
        )
        
        filters['radius'] = st.sidebar.slider(
            "Search radius (km)",
            1, 20, 5,
            help="How far are you willing to travel?"
        ) * 1000  # Convert to meters
        
        # Buy me coffee button
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ☕ Support This Project")
        st.sidebar.markdown(
            f'<a href="{BUY_ME_COFFEE_URL}" target="_blank">'
            '<button style="background-color:#FFDD44; border:none; padding:10px 20px; '
            'border-radius:5px; cursor:pointer; width:100%;">'
            '☕ Buy Me a Coffee!'
            '</button></a>',
            unsafe_allow_html=True
        )
        
        return filters
    
    def run(self):
        """Main application logic"""
        # Check API keys - show warning but don't stop app
        missing_keys = Config.validate_keys()
        if missing_keys:
            st.warning(f"Running in demo mode. Missing API keys: {', '.join(missing_keys)}")
            st.info("💡 Add API keys to .env file for full functionality. App works with fallback data!")
        
        # Header
        st.markdown('<h1 class="main-header">🗺️ Bored Go Where SG</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Your AI companion for discovering Singapore when boredom strikes!</p>', unsafe_allow_html=True)
        
        # Initialize session state
        if 'conversation' not in st.session_state:
            st.session_state.conversation = []
        if 'current_places' not in st.session_state:
            st.session_state.current_places = []
        
        # Sidebar filters
        filters = self.sidebar_filters()
        
        # Main chat interface
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("💬 Chat with me!")
            
            # Display conversation
            for role, message in st.session_state.conversation:
                with st.chat_message(role):
                    st.write(message)
            
            # Chat input
            user_input = st.chat_input("Tell me you're bored, or ask for suggestions!")
            
            if user_input:
                # Add user message
                st.session_state.conversation.append(("user", user_input))
                
                with st.chat_message("user"):
                    st.write(user_input)
                
                # Process request
                with st.spinner("Finding amazing places for you..."):
                    intent = self.parse_user_intent(user_input)
                    
                    # Search places
                    places = self.engine.search_places(
                        query=intent['query'],
                        radius=filters['radius']
                    )
                    
                    # Apply filters
                    places = self.engine.filter_by_mood(places, filters['mood'])
                    places = self.engine.filter_by_budget(places, filters['budget'])
                    
                    # Limit to top 5
                    places = places[:5]
                    st.session_state.current_places = places
                    
                    # Generate AI response
                    ai_response = self.generate_ai_response(places, user_input)
                    st.session_state.conversation.append(("assistant", ai_response))
                
                with st.chat_message("assistant"):
                    st.write(ai_response)
                
                # Display place cards
                if places:
                    st.subheader("📍 Suggested Places")
                    self.display_place_cards(places)
        
        with col2:
            st.subheader("🗺️ Map View")
            
            if st.session_state.current_places:
                # Create and display map
                map_obj = self.create_map(st.session_state.current_places)
                st_folium(map_obj, width=700, height=600)
            else:
                # Default Singapore map
                default_map = folium.Map(
                    location=[SINGAPORE_CENTER['lat'], SINGAPORE_CENTER['lon']],
                    zoom_start=11
                )
                st_folium(default_map, width=700, height=600)
                st.info("🗺️ Start chatting to see places on the map!")

# Run the app
if __name__ == "__main__":
    app = BoredGoWhereApp()
    app.run()