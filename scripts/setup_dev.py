#!/usr/bin/env python3
"""
Development environment setup script.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run a command and print its output."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result


def setup_dev_environment():
    """Set up the development environment."""
    print("🚀 Setting up Markdown Manager development environment...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install package in development mode
    print("\n📦 Installing package in development mode...")
    run_command([sys.executable, "-m", "pip", "install", "-e", ".[dev,test]"])
    
    # Install pre-commit hooks
    print("\n🔧 Installing pre-commit hooks...")
    run_command(["pre-commit", "install"])
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 Creating .env file from template...")
        import shutil
        shutil.copy(env_example, env_file)
        print("⚠️  Please edit .env file with your Azure credentials")
    
    # Create necessary directories
    print("\n📁 Creating necessary directories...")
    directories = ["logs", "sessions", "data"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   Created: {dir_name}/")
    
    # Run initial tests
    print("\n🧪 Running initial tests...")
    try:
        run_command([sys.executable, "-m", "pytest", "--version"])
        run_command([sys.executable, "-m", "pytest", "-v", "tests/", "--tb=short"])
        print("✅ All tests passed!")
    except subprocess.CalledProcessError:
        print("⚠️  Some tests failed, but that's okay for initial setup")
    
    print("\n🎉 Development environment setup complete!")
    print("\n📖 Next steps:")
    print("   1. Edit .env file with your Azure credentials")
    print("   2. Run 'make run-dev' to start the application")
    print("   3. Run 'make test' to run the test suite")
    print("   4. Run 'make format' to format your code")
    print("   5. Check out CONTRIBUTING.md for more details")


if __name__ == "__main__":
    setup_dev_environment()