#!/usr/bin/env python3
"""
Build script for creating professional Windows installer using Inno Setup.
This script automates the entire process: exe build -> icon creation -> installer creation.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def run_command(cmd, check=True, shell=False):
    """Run a command and print its output."""
    if isinstance(cmd, str) and not shell:
        # If it's a string and we're not using shell, split it
        cmd = cmd.split()
    
    print(f"Running: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, check=check, capture_output=True, text=True, shell=shell)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result


def find_inno_setup():
    """Find Inno Setup installation."""
    possible_paths = [
        "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe",
        "C:\\Program Files\\Inno Setup 6\\ISCC.exe", 
        "C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe",
        "C:\\Program Files\\Inno Setup 5\\ISCC.exe",
    ]
    
    for path in possible_paths:
        if Path(path).exists():
            return path
    
    return None


def install_inno_setup():
    """Guide user to install Inno Setup."""
    print("Inno Setup not found!")
    print("\nTo create professional installers, you need Inno Setup:")
    print("1. Download from: https://jrsoftware.org/isdl.php")
    print("2. Install Inno Setup 6")
    print("3. Run this script again")
    print("\nAlternatively, you can:")
    print("- Use the simple batch installer: dist/install.bat")
    print("- Distribute just the .exe file")
    return False


def create_icon():
    """Create application icon if it doesn't exist."""
    icon_path = Path("assets/icon.ico")
    if icon_path.exists():
        print("Icon already exists")
        return True
    
    print("Creating application icon...")
    try:
        # Try to run the icon creation script
        run_command([sys.executable, "assets/create_icon.py"])
        if icon_path.exists():
            print("Icon created successfully")
            return True
        else:
            print("WARNING: Icon creation failed, installer will use default")
            return False
    except Exception as e:
        print(f"WARNING: Icon creation failed: {e}")
        return False


def build_executable():
    """Check if executable exists or build it."""
    print("Checking for executable...")
    
    exe_path = Path("dist/MarkdownManager.exe")
    if exe_path.exists():
        print(f"Executable found: {exe_path}")
        print(f"File size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
        return True
    
    print("Building executable...")
    # Run the existing build script
    try:
        run_command([sys.executable, "scripts/build_exe.py"])
        
        if exe_path.exists():
            print("Executable built successfully")
            return True
        else:
            print("ERROR: Executable build failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Executable build failed: {e}")
        return False


def create_installer():
    """Create the installer using Inno Setup."""
    print("Creating installer...")
    
    # Find Inno Setup
    iscc_path = find_inno_setup()
    if not iscc_path:
        return install_inno_setup()
    
    print(f"Found Inno Setup: {iscc_path}")
    
    # Build installer
    iss_file = Path("installer/MarkdownManager.iss")
    if not iss_file.exists():
        print("ERROR: Installer script not found!")
        return False
    
    try:
        # Run Inno Setup compiler
        result = run_command([iscc_path, str(iss_file)], check=False)
        
        # Check if installer was created
        installer_dir = Path("installer/output")
        if installer_dir.exists():
            installers = list(installer_dir.glob("*.exe"))
            if installers:
                installer_path = installers[0]
                print(f"Installer created: {installer_path}")
                print(f"File size: {installer_path.stat().st_size / (1024*1024):.1f} MB")
                
                # Test installer signature (basic check)
                print("Testing installer...")
                try:
                    # Just check if it's a valid PE file
                    with open(installer_path, 'rb') as f:
                        header = f.read(2)
                        if header == b'MZ':
                            print("Installer appears to be valid")
                        else:
                            print("WARNING: Installer may be corrupted")
                except:
                    print("WARNING: Could not validate installer")
                
                return True
        
        print("ERROR: Installer creation failed")
        if result.returncode != 0:
            print(f"Inno Setup exit code: {result.returncode}")
        return False
        
    except Exception as e:
        print(f"ERROR: Installer creation failed: {e}")
        return False


def create_release_package():
    """Create a complete release package."""
    print("Creating release package...")
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy installer
    installer_dir = Path("installer/output")
    installers = list(installer_dir.glob("*.exe"))
    if installers:
        installer_src = installers[0]
        installer_dest = release_dir / installer_src.name
        shutil.copy2(installer_src, installer_dest)
        print(f"Copied installer: {installer_dest.name}")
    
    # Copy standalone executable
    exe_src = Path("dist/MarkdownManager.exe")
    if exe_src.exists():
        exe_dest = release_dir / "MarkdownManager-Standalone.exe"
        shutil.copy2(exe_src, exe_dest)
        print(f"Copied standalone exe: {exe_dest.name}")
    
    # Copy documentation
    docs = [
        ("README.md", "README.txt"),
        ("CHANGELOG.md", "CHANGELOG.txt"),
        (".env.example", ".env.example"),
        ("installer/LICENSE.txt", "LICENSE.txt")
    ]
    
    for src, dest in docs:
        src_path = Path(src)
        if src_path.exists():
            dest_path = release_dir / dest
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {dest}")
    
    # Create release notes
    release_notes = f"""# Markdown Manager v1.2.0 - Release Package

## What's Included

### Professional Installer (Recommended)
- `MarkdownManager-Setup-v1.2.0.exe` - Full installer with shortcuts and uninstaller
- Installs to Program Files with Start Menu integration
- Includes all documentation and sample files
- Optional desktop shortcut and PATH integration

### Standalone Executable  
- `MarkdownManager-Standalone.exe` - Portable version, no installation needed
- Just download and run, no admin rights required
- All features included in single file

### Documentation
- `README.txt` - Complete user guide and feature documentation
- `CHANGELOG.txt` - Version history and updates
- `LICENSE.txt` - MIT license terms
- `.env.example` - Configuration template for AI features

## Quick Start

### Option 1: Use the Installer (Recommended for most users)
1. Download `MarkdownManager-Setup-v1.2.0.exe`
2. Run the installer (Windows may ask for permission)
3. Follow the setup wizard
4. Launch from Start Menu or Desktop shortcut

### Option 2: Use Standalone Version
1. Download `MarkdownManager-Standalone.exe`
2. Save to desired folder
3. Double-click to run
4. First startup may take 15-30 seconds

## Configuration

### Basic Usage
- No configuration needed for basic markdown viewing and editing
- Sample files included for testing

### AI Features (Optional)
1. Create `.env` file using the provided template
2. Add your Azure OpenAI credentials
3. Restart the application

### Cloud Sync (Optional)
- Configure Azure Blob Storage connection string
- Two-way sync between local files and cloud storage

## Support

- **Documentation**: Full README.txt included
- **Issues**: https://github.com/jeremy-schaab/MarkdownTool/issues
- **Updates**: https://github.com/jeremy-schaab/MarkdownTool/releases

## System Requirements

- Windows 7, 8, 10, or 11
- 500MB free disk space
- Internet connection (for AI features only)

---
Built with love for the markdown community
"""
    
    release_notes_path = release_dir / "RELEASE-NOTES.txt"
    release_notes_path.write_text(release_notes, encoding='utf-8')
    print(f"Created: RELEASE-NOTES.txt")
    
    # Create ZIP package
    zip_name = f"MarkdownManager-v1.2.0-Complete"
    print(f"Creating ZIP package: {zip_name}.zip")
    shutil.make_archive(zip_name, 'zip', release_dir)
    
    final_zip = Path(f"{zip_name}.zip")
    if final_zip.exists():
        print(f"ZIP package created: {final_zip}")
        print(f"ZIP size: {final_zip.stat().st_size / (1024*1024):.1f} MB")
    
    return True


def main():
    """Main build function."""
    print("Markdown Manager - Professional Installer Builder")
    print("=" * 60)
    
    if os.name != 'nt':
        print("WARNING: This script is designed for Windows")
        print("    The installer will only work on Windows systems")
    
    # Step 1: Create icon
    print("\nStep 1: Create Application Icon")
    create_icon()
    
    # Step 2: Build executable
    print("\nStep 2: Build Executable")
    if not build_executable():
        print("ERROR: Cannot continue without executable")
        sys.exit(1)
    
    # Step 3: Create installer
    print("\nStep 3: Create Professional Installer")
    installer_created = create_installer()
    
    # Step 4: Create release package
    print("\nStep 4: Create Release Package")
    create_release_package()
    
    # Summary
    print("\n" + "=" * 60)
    if installer_created:
        print("SUCCESS! Professional installer created")
        print("\nRelease Files Created:")
        print("   - Professional Installer: installer/output/MarkdownManager-Setup-v1.2.0.exe")
        print("   - Standalone Executable: release/MarkdownManager-Standalone.exe") 
        print("   - Complete ZIP Package: MarkdownManager-v1.2.0-Complete.zip")
        print("   - Documentation: release/ folder")
        
        print("\nDistribution Options:")
        print("   1. Share the installer exe for easy installation")
        print("   2. Share the standalone exe for portable use")
        print("   3. Share the complete ZIP for everything")
        
        print("\nRecommended: Upload the installer to your GitHub releases!")
        
    else:
        print("WARNING: Installer creation failed, but standalone exe is available")
        print("   - Standalone Executable: release/MarkdownManager-Standalone.exe")
        print("   - You can still distribute the standalone version")
        
        print("\nTo create professional installer:")
        print("   1. Install Inno Setup from https://jrsoftware.org/isdl.php")
        print("   2. Run this script again")


if __name__ == "__main__":
    main()