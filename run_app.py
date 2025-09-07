#!/usr/bin/env python3
"""
Legacy runner script for backward compatibility.
This script now uses the new package structure.
"""

import subprocess
import sys
import warnings
from pathlib import Path


def main():
    """Main function to run the Streamlit app."""
    warnings.warn(
        "run_app.py is deprecated. Use 'markdown-manager' command instead.",
        DeprecationWarning,
        stacklevel=2
    )
    
    # Get the path to the app file in the new structure
    app_path = Path(__file__).parent / "src" / "markdown_manager" / "app.py"
    
    # Check if the app file exists
    if not app_path.exists():
        print(f"Error: {app_path} not found!")
        print("Try running 'markdown-manager' command instead.")
        sys.exit(1)
    
    # Run the Streamlit app
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        str(app_path), 
        "--server.port", "8501"
    ]
    
    try:
        print("🚀 Starting Markdown Manager (legacy mode)...")
        print(f"   App will be available at: http://localhost:8501")
        print("   Press Ctrl+C to stop the application")
        print("   💡 Tip: Use 'markdown-manager' command for better experience")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()