# 🗺️ Bored Go Where Singapore

![Banner](https://i.ibb.co/y49126P/bg3.png)

## 🎯 Project Overview

**Bored Go Where SG** is an AI-powered interactive web application that helps users discover exciting places and activities in Singapore when boredom strikes. Using a conversational chat interface, the app suggests personalized recommendations based on mood, budget, weather, and preferences.

## ✨ Key Features

- 💬 **Conversational Chat Interface** - Natural language input for queries like "I'm bored" or "Weekend ideas?"
- 🗺️ **Interactive Map Visualization** - Live map with numbered markers for suggested places
- 🌤️ **Weather Integration** - Real-time weather data to avoid outdoor spots during rain
- 🎭 **Mood-Based Filtering** - Suggestions based on mood (chill, active, romantic, cultural, random)
- 💰 **Budget Awareness** - Filter by price range (free, cheap, moderate, splurge)
- 📍 **Location Intelligence** - Smart suggestions based on proximity and travel time
- ☕ **Support Integration** - "Buy Me a Coffee" button for project support

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API Keys for:
  - OpenAI (for AI responses)
  - Google Places (for place data)
  - OpenWeather (for weather data)

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd Bored_Go_Where_SG
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure API Keys**:
   ```bash
   cp .env.example .env
   # Edit .env file with your actual API keys
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🔧 Configuration

### API Keys Setup

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_api_key_here
MAPBOX_ACCESS_TOKEN=your_mapbox_token_here
GOOGLE_PLACES_API_KEY=your_google_places_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

### Getting API Keys

1. **OpenAI**: Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Google Places**: Visit [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
3. **OpenWeather**: Visit [OpenWeatherMap](https://openweathermap.org/api)

## 📁 Project Structure

```
Bored_Go_Where_SG/
├── app.py                 # Main Streamlit application
├── place_engine.py        # Place suggestion logic and API integration
├── config.py             # Configuration and API key management
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
└── assets/              # Image assets and mockups
```

## 🎮 How to Use

1. **Start the app** and open in your browser
2. **Type your query** in the chat input:
   - "I'm bored"
   - "Looking for romantic date ideas"
   - "Free activities near Marina Bay"
   - "Rainy day indoor activities"
3. **Adjust filters** in the sidebar:
   - Select your mood
   - Set budget preference
   - Choose search radius
4. **Explore suggestions** on the map and in the chat
5. **Get details** about each place including weather conditions

## 🛠️ Technical Stack

- **Frontend**: Streamlit with custom CSS
- **Maps**: Folium for interactive mapping
- **AI**: OpenAI GPT for conversational responses
- **APIs**: Google Places, OpenWeather
- **Deployment**: Streamlit Cloud ready

## 🎯 Roadmap

- [x] Core chat interface
- [x] Place suggestion engine
- [x] Map visualization
- [x] Weather integration
- [x] Filter system
- [x] Buy Me a Coffee integration
- [ ] Route optimization for multiple stops
- [ ] User session memory
- [ ] Advanced NLP for better intent recognition
- [ ] Offline fallback data
- [ ] Mobile responsiveness improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## ☕ Support

If you find this project helpful, consider supporting it:

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/yourusername)

## 📞 Contact

Created with ❤️ to solve the eternal question: "Bored... go where?"

---

**Note**: This project uses free-tier APIs. For production use, consider upgrading to paid tiers for better rate limits and features.