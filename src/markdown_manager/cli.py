#!/usr/bin/env python3
"""
Command-line interface for Markdown Manager.
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Main entry point for the CLI."""
    try:
        # Get the path to the app module
        app_path = Path(__file__).parent / "app.py"
        
        # Run streamlit with the app
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(app_path), 
            "--server.port", "8501",
            "--server.headless", "true"
        ]
        
        print("🚀 Starting Markdown Manager...")
        print(f"   Opening at: http://localhost:8501")
        print("   Press Ctrl+C to stop")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()