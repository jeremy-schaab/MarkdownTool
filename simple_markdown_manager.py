#!/usr/bin/env python3
"""
Simple standalone version of Markdown Manager for quick executable build.
This is a simplified version that can be packaged quickly.
"""

import sys
import subprocess
import os
from pathlib import Path


def main():
    """Simple main function that launches the full application."""
    print("Markdown Manager v1.2.0")
    print("Starting application...")
    
    try:
        # Try to find the main application
        app_paths = [
            Path(__file__).parent / "src" / "markdown_manager" / "app.py",
            Path(__file__).parent / "markdown_viewer.py",  # fallback
        ]
        
        app_file = None
        for path in app_paths:
            if path.exists():
                app_file = str(path)
                break
        
        if not app_file:
            print("Error: Could not find main application file")
            input("Press Enter to exit...")
            return
        
        # Launch Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            app_file, 
            "--server.port", "8501"
        ]
        
        print("Opening Markdown Manager at http://localhost:8501")
        print("Press Ctrl+C to stop the application")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except FileNotFoundError:
        print("Error: Streamlit not found. Please install required dependencies.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()