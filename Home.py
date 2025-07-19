import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Bored Go Where SG",
    page_icon="🗺️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #FF6B6B;
        font-size: 4em;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.5em;
        margin-bottom: 2em;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
    }
    .setup-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🗺️ Bored Go Where SG</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI companion for discovering Singapore when boredom strikes!</p>', unsafe_allow_html=True)
    
    # Hero image
    st.image("https://i.ibb.co/y49126P/bg3.png", use_container_width=True)
    
    # Check setup status
    if st.session_state.get('api_setup_complete', False):
        st.success("✅ Setup Complete! Ready to discover amazing places.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Start Exploring", type="primary", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button("🔧 Manage APIs", use_container_width=True):
                st.switch_page("pages/1_🔧_API_Setup.py")
    else:
        # Setup required
        st.markdown("""
        <div class="setup-card">
            <h2>🚀 Welcome to Bored Go Where SG!</h2>
            <p>To get started, you'll need to set up your API credentials.</p>
            <p>Don't worry - all APIs have free tiers!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔧 Setup APIs Now", type="primary", use_container_width=True):
            st.switch_page("pages/1_🔧_API_Setup.py")
    
    # Features overview
    st.subheader("✨ What can this app do?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Smart Chat</h3>
            <p>Talk naturally: "I'm bored", "romantic date ideas", "free outdoor activities"</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🗺️ Live Map</h3>
            <p>See suggestions on an interactive map with weather info and directions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Smart Filters</h3>
            <p>Filter by mood, budget, time of day, and distance preferences</p>
        </div>
        """, unsafe_allow_html=True)
    
    # API Info
    st.subheader("🔑 Required APIs (All Free!)")
    
    api_info = [
        ("🤖 OpenAI", "Powers intelligent chat responses", "https://platform.openai.com/api-keys"),
        ("🗺️ Google Places", "Provides real place data and reviews", "https://console.cloud.google.com/apis/credentials"),
        ("🌤️ OpenWeather", "Shows current weather conditions", "https://openweathermap.org/api")
    ]
    
    for icon, description, link in api_info:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.markdown(f"**{icon}**")
        with col2:
            st.markdown(description)
        with col3:
            st.markdown(f"[Get Key]({link})")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2em;">
        Created with ❤️ to solve the eternal question: "Bored... go where?"<br>
        <a href="https://www.buymeacoffee.com/yourusername" target="_blank">☕ Buy me a coffee</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()