#!/usr/bin/env python3
"""
Enhanced GeoGPT Streamlit App Launcher
"""

import subprocess
import sys
import os

def main():
    """Launch the enhanced Streamlit app"""
    print("🚀 Launching Enhanced GeoGPT Streamlit App...")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Check for additional dependencies
    try:
        import requests
        print("✅ Requests is installed")
    except ImportError:
        print("❌ Installing requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    
    # Launch the app
    print("\n🌍 Starting Enhanced GeoGPT App...")
    print("📱 Open your browser to: http://localhost:8501")
    print("🔑 Make sure to add your API keys in the sidebar")
    print("\n" + "=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app_enhanced.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main()
