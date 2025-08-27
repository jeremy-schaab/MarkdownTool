#!/usr/bin/env python3
"""
Simple script to run the Markdown Viewer Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_file = os.path.join(script_dir, "markdown_viewer.py")
    
    if not os.path.exists(app_file):
        print(f"Error: {app_file} not found!")
        sys.exit(1)
    
    print("Starting Markdown Viewer...")
    print("Open your browser and go to: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            app_file, "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except FileNotFoundError:
        print("Error: Streamlit not found. Please install it with: pip install streamlit")
        sys.exit(1)

if __name__ == "__main__":
    main()