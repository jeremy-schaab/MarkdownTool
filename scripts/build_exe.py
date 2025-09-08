#!/usr/bin/env python3
"""
Build script for creating Windows executable using PyInstaller.
"""

import os
import sys
import shutil
import subprocess
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


def create_default_icon():
    """Create a simple default icon if none exists."""
    icon_path = Path("assets/icon.ico")
    if not icon_path.exists():
        print("⚠️  No icon found, creating placeholder...")
        # You can replace this with actual icon creation logic
        # For now, we'll modify the spec to not require an icon
        return False
    return True


def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller"])


def build_executable():
    """Build the Windows executable."""
    print("Building Markdown Manager executable...")
    
    # Clean previous builds
    build_dirs = ["build", "dist"]
    for dir_name in build_dirs:
        if Path(dir_name).exists():
            print(f"Cleaning {dir_name}/")
            shutil.rmtree(dir_name)
    
    # Check for icon
    has_icon = create_default_icon()
    
    # Modify spec file if no icon
    spec_content = Path("markdown_manager.spec").read_text()
    if not has_icon:
        spec_content = spec_content.replace("icon='assets/icon.ico',", "# icon='assets/icon.ico',")
        Path("markdown_manager.spec").write_text(spec_content)
        print("WARNING: Building without icon (you can add assets/icon.ico later)")
    
    # Build with PyInstaller
    try:
        run_command([sys.executable, "-m", "PyInstaller", "markdown_manager.spec"])
        
        # Check if build was successful
        exe_path = Path("dist/MarkdownManager.exe")
        if exe_path.exists():
            print(f"Build successful!")
            print(f"Executable created: {exe_path.absolute()}")
            print(f"File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            
            # Test the executable
            print("Testing executable...")
            try:
                result = run_command([str(exe_path), "--help"], check=False)
                if result.returncode == 0:
                    print("Executable test passed")
                else:
                    print("WARNING: Executable test failed, but file was created")
            except Exception as e:
                print(f"WARNING: Could not test executable: {e}")
                
        else:
            print("ERROR: Build failed - executable not found")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Build failed: {e}")
        return False
    
    return True


def create_installer_script():
    """Create a simple installer script."""
    installer_content = """@echo off
echo Installing Markdown Manager...

REM Create installation directory
set INSTALL_DIR=%LOCALAPPDATA%\\MarkdownManager
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy executable
copy "MarkdownManager.exe" "%INSTALL_DIR%\\MarkdownManager.exe"

REM Create desktop shortcut
set DESKTOP=%USERPROFILE%\\Desktop
echo [InternetShortcut] > "%DESKTOP%\\Markdown Manager.url"
echo URL=file:///%INSTALL_DIR%\\MarkdownManager.exe >> "%DESKTOP%\\Markdown Manager.url"
echo IconFile=%INSTALL_DIR%\\MarkdownManager.exe >> "%DESKTOP%\\Markdown Manager.url"
echo IconIndex=0 >> "%DESKTOP%\\Markdown Manager.url"

REM Create start menu shortcut
set STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs
echo [InternetShortcut] > "%STARTMENU%\\Markdown Manager.url"
echo URL=file:///%INSTALL_DIR%\\MarkdownManager.exe >> "%STARTMENU%\\Markdown Manager.url"
echo IconFile=%INSTALL_DIR%\\MarkdownManager.exe >> "%STARTMENU%\\Markdown Manager.url"
echo IconIndex=0 >> "%STARTMENU%\\Markdown Manager.url"

echo Installation complete!
echo You can now run Markdown Manager from the Start Menu or Desktop shortcut.
pause
"""
    
    installer_path = Path("dist/install.bat")
    installer_path.write_text(installer_content)
    print(f"Created installer script: {installer_path}")


def main():
    """Main build function."""
    print("Markdown Manager - Windows Executable Builder")
    print("=" * 50)
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("WARNING: This script is designed for Windows. You can still build, but the executable will be for the current platform.")
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    if build_executable():
        print("\nBuild completed successfully!")
        print("\nNext steps:")
        print("   1. Test the executable: dist/MarkdownManager.exe")
        print("   2. Run installer: dist/install.bat (optional)")
        print("   3. Distribute the dist/ folder or just the .exe file")
        print("\nTips:")
        print("   - Add assets/icon.ico for a custom icon")
        print("   - The first run may be slower as it extracts files")
        print("   - Include .env.example for users to configure AI features")
        
        # Create installer script
        create_installer_script()
        
    else:
        print("\nBuild failed!")
        print("Check the error messages above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()