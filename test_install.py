#!/usr/bin/env python3
"""Test script to check if all dependencies are available"""

print("Testing dependencies...")

try:
    import streamlit as st
    print("OK - Streamlit imported successfully")
except ImportError as e:
    print(f"FAIL - Streamlit import failed: {e}")

try:
    import folium
    print("OK - Folium imported successfully")
except ImportError as e:
    print(f"FAIL - Folium import failed: {e}")

try:
    import requests
    print("OK - Requests imported successfully")
except ImportError as e:
    print(f"FAIL - Requests import failed: {e}")

try:
    import openai
    print("OK - OpenAI imported successfully")
except ImportError as e:
    print(f"FAIL - OpenAI import failed: {e}")

print("\nIf all imports succeeded, you can run: python -m streamlit run app.py")
print("Alternative: streamlit run app.py")