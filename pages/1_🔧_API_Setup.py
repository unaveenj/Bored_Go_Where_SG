import streamlit as st
import time
from api_validator import APIValidator
from config import Config

# Page configuration
st.set_page_config(
    page_title="API Setup - Bored Go Where SG",
    page_icon="🔧",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .api-status {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-weight: bold;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .status-testing {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    .credentials-form {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🔧 API Setup")
    st.markdown("Configure your API credentials to unlock the full potential of Bored Go Where SG!")
    
    # Initialize validator
    validator = APIValidator()
    
    # Check if setup is already complete
    if st.session_state.get('api_setup_complete', False):
        st.success("✅ API setup is complete! You can now use the main app.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Go to Main App", type="primary", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            if st.button("🔄 Reconfigure APIs", use_container_width=True):
                st.session_state['api_setup_complete'] = False
                st.rerun()
        
        # Show current status
        st.subheader("Current API Status")
        show_api_status()
        return
    
    # Introduction
    st.info("""
    🎯 **Why do I need API keys?**
    - **OpenAI**: Powers the intelligent chat responses
    - **Google Places**: Provides real place data and reviews
    - **OpenWeather**: Shows current weather conditions
    
    💡 **All APIs offer free tiers!** Get your keys from the links below.
    """)
    
    # API Keys Input Form
    st.subheader("📝 Enter Your API Keys")
    
    with st.container():
        st.markdown('<div class="credentials-form">', unsafe_allow_html=True)
        
        # OpenAI API Key
        st.markdown("**🤖 OpenAI API Key**")
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Get your free API key from: https://platform.openai.com/api-keys",
            label_visibility="collapsed"
        )
        st.markdown("[Get OpenAI API Key](https://platform.openai.com/api-keys) 🔗")
        
        st.divider()
        
        # Google Places API Key
        st.markdown("**🗺️ Google Places API Key**")
        google_key = st.text_input(
            "Google Places API Key",
            type="password",
            placeholder="AIza...",
            help="Get your free API key from Google Cloud Console",
            label_visibility="collapsed"
        )
        st.markdown("[Get Google Places API Key](https://console.cloud.google.com/apis/credentials) 🔗")
        
        st.divider()
        
        # OpenWeather API Key
        st.markdown("**🌤️ OpenWeather API Key**")
        weather_key = st.text_input(
            "OpenWeather API Key",
            type="password",
            placeholder="abc123...",
            help="Get your free API key from OpenWeatherMap",
            label_visibility="collapsed"
        )
        st.markdown("[Get OpenWeather API Key](https://openweathermap.org/api) 🔗")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Buttons
    st.subheader("🧪 Test Your APIs")
    
    col1, col2, col3 = st.columns(3)
    
    credentials = {
        'openai': openai_key,
        'google_places': google_key,
        'openweather': weather_key
    }
    
    # Individual API testing
    with col1:
        if st.button("Test OpenAI", disabled=not openai_key, use_container_width=True):
            test_individual_api('openai', openai_key, validator)
    
    with col2:
        if st.button("Test Google Places", disabled=not google_key, use_container_width=True):
            test_individual_api('google_places', google_key, validator)
    
    with col3:
        if st.button("Test OpenWeather", disabled=not weather_key, use_container_width=True):
            test_individual_api('openweather', weather_key, validator)
    
    st.divider()
    
    # Test all APIs
    all_keys_provided = all(credentials.values())
    
    if st.button(
        "🚀 Test All APIs & Continue",
        type="primary",
        disabled=not all_keys_provided,
        use_container_width=True
    ):
        test_all_apis(credentials, validator)
    
    if not all_keys_provided:
        st.warning("⚠️ Please provide all API keys to continue")
    
    # Show current test results
    if 'api_test_results' in st.session_state:
        st.subheader("🔍 Test Results")
        show_test_results(st.session_state['api_test_results'])

def test_individual_api(api_name: str, api_key: str, validator: APIValidator):
    """Test individual API and show results"""
    with st.spinner(f"Testing {api_name.replace('_', ' ').title()} API..."):
        if api_name == 'openai':
            success, message = validator.test_openai_api(api_key)
        elif api_name == 'google_places':
            success, message = validator.test_google_places_api(api_key)
        elif api_name == 'openweather':
            success, message = validator.test_openweather_api(api_key)
        else:
            success, message = False, "Unknown API"
        
        # Store individual result
        if 'api_test_results' not in st.session_state:
            st.session_state['api_test_results'] = {}
        
        st.session_state['api_test_results'][api_name] = (success, message)
        
        if success:
            st.success(f"✅ {api_name.replace('_', ' ').title()}: {message}")
        else:
            st.error(f"❌ {api_name.replace('_', ' ').title()}: {message}")

def test_all_apis(credentials: dict, validator: APIValidator):
    """Test all APIs and proceed if successful"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Test each API with progress updates
    results = {}
    apis = list(credentials.keys())
    
    for i, (api_name, api_key) in enumerate(credentials.items()):
        status_text.text(f"Testing {api_name.replace('_', ' ').title()} API...")
        progress_bar.progress((i + 1) / len(apis))
        
        if api_name == 'openai':
            success, message = validator.test_openai_api(api_key)
        elif api_name == 'google_places':
            success, message = validator.test_google_places_api(api_key)
        elif api_name == 'openweather':
            success, message = validator.test_openweather_api(api_key)
        else:
            success, message = False, "Unknown API"
        
        results[api_name] = (success, message)
        time.sleep(0.5)  # Small delay for visual effect
    
    status_text.empty()
    progress_bar.empty()
    
    # Store results
    st.session_state['api_test_results'] = results
    
    # Check if all APIs passed
    all_passed = all(success for success, _ in results.values())
    
    if all_passed:
        st.success("🎉 All APIs are working perfectly!")
        
        # Save credentials to session
        validator.save_credentials_to_session(credentials)
        
        # Success actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Go to Main App", type="primary", use_container_width=True):
                st.switch_page("app.py")
        with col2:
            st.success("Setup Complete! ✅")
    else:
        st.error("❌ Some APIs failed. Please check your credentials and try again.")
        show_test_results(results)

def show_test_results(results: dict):
    """Display test results in a formatted way"""
    for api_name, (success, message) in results.items():
        api_display = api_name.replace('_', ' ').title()
        
        if success:
            st.markdown(f"""
            <div class="api-status status-success">
                ✅ {api_display}: {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="api-status status-error">
                ❌ {api_display}: {message}
            </div>
            """, unsafe_allow_html=True)

def show_api_status():
    """Show current API status from session"""
    credentials = {
        'openai': st.session_state.get('api_openai', ''),
        'google_places': st.session_state.get('api_google_places', ''),
        'openweather': st.session_state.get('api_openweather', '')
    }
    
    for api_name, api_key in credentials.items():
        api_display = api_name.replace('_', ' ').title()
        if api_key:
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            st.markdown(f"""
            <div class="api-status status-success">
                ✅ {api_display}: Connected ({masked_key})
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="api-status status-error">
                ❌ {api_display}: Not configured
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()