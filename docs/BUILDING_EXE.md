# Building Windows Executable

This guide explains how to create a standalone Windows executable (.exe) file for Markdown Manager that users can run without installing Python or dependencies.

## 🚀 Quick Start

### Option 1: Using the Build Script (Recommended)
```bash
# Run the automated build script
python scripts/build_exe.py

# Or use the Windows batch file
scripts\build_exe.bat
```

### Option 2: Manual Build with PyInstaller
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller markdown_manager.spec
```

## 📋 Prerequisites

- **Python 3.8+** installed on Windows
- **All project dependencies** installed (`pip install -e .`)
- **PyInstaller** (will be installed automatically by build script)

## 🛠️ Build Process Details

### What the Build Script Does

1. **Installs PyInstaller** if not already present
2. **Cleans previous builds** (removes `build/` and `dist/` folders)
3. **Builds executable** using the configured spec file
4. **Tests the executable** to ensure it works
5. **Creates installer script** for easy deployment
6. **Reports file size** and build status

### Build Configuration

The build is configured in `markdown_manager.spec` which includes:

- **Entry point**: `src/markdown_manager/cli.py`
- **Data files**: Configuration, test files, documentation
- **Hidden imports**: All Streamlit and dependency modules
- **Excluded modules**: Development and testing tools
- **Version information**: Windows version metadata
- **Icon support**: Custom icon (if provided)

## 📁 Output Structure

After building, you'll find:

```
dist/
├── MarkdownManager.exe     # Main executable (~150-200MB)
└── install.bat            # Optional installer script
```

## 🎯 Using the Executable

### Running the Executable
```bash
# Run directly
MarkdownManager.exe

# Or double-click in Windows Explorer
```

### First Run Notes
- **Startup time**: First run may be slower (15-30 seconds) as files are extracted
- **Windows Defender**: May need to allow the executable through Windows Defender
- **Temporary files**: Creates temporary files in system temp directory during execution

### Configuration
- **Environment file**: Place `.env` file in the same directory as the executable
- **Data directory**: Executable will create `data/`, `logs/`, and `sessions/` folders
- **Test files**: Included test files are available for demo purposes

## 📦 Distribution Options

### Option 1: Single File Distribution
- **File**: Just distribute `MarkdownManager.exe`
- **Size**: ~150-200MB
- **Pros**: Simple, single file
- **Cons**: Large file size, slower startup

### Option 2: Directory Distribution
```bash
# Modify spec file to create directory distribution
# Change: onefile=True to onefile=False
pyinstaller markdown_manager.spec
```
- **Output**: `dist/MarkdownManager/` folder with multiple files
- **Pros**: Faster startup, smaller individual files
- **Cons**: Multiple files to distribute

### Option 3: Installer Package
Use the provided `install.bat` script or create a proper installer:

#### Using install.bat
1. Copy `MarkdownManager.exe` and `install.bat` to user's computer
2. Run `install.bat` as administrator
3. Creates shortcuts on Desktop and Start Menu

#### Professional Installer (Advanced)
Consider using tools like:
- **Inno Setup** (free)
- **NSIS** (free)
- **WiX Toolset** (free)
- **InstallShield** (commercial)

## 🔧 Customization Options

### Adding Custom Icon
1. **Create icon**: Create or find a `.ico` file (32x32, 48x48, 64x64 pixels recommended)
2. **Save as**: `assets/icon.ico`
3. **Rebuild**: Run the build script again

### Modifying Build Settings

Edit `markdown_manager.spec` to customize:

```python
# Console vs Windowed application
console=True,  # Set to False for windowed app (no console window)

# Enable/disable UPX compression
upx=True,  # Set to False to disable compression (larger file, faster startup)

# Add additional data files
datas=[
    ('your_custom_files', 'destination'),
],

# Add additional hidden imports
hiddenimports=[
    'your_custom_module',
],
```

### Build Variations

#### Debug Build
```python
# In markdown_manager.spec
debug=True,  # Enables debug output
console=True,  # Keep console for debug info
```

#### Optimized Build
```python
# In markdown_manager.spec
upx=True,  # Enable compression
strip=True,  # Strip debug symbols
optimize=2,  # Python optimization level
```

## 🧪 Testing the Executable

### Automated Testing
The build script automatically tests the executable:
```bash
# Test help command
MarkdownManager.exe --help
```

### Manual Testing
```bash
# Test basic functionality
cd dist
MarkdownManager.exe

# Test with environment variables
set STREAMLIT_PORT=8502
MarkdownManager.exe

# Test with custom folder
MarkdownManager.exe
# Then browse to your test files in the UI
```

### Common Issues and Solutions

**"Failed to execute script"**
- Missing dependencies in spec file
- Add to `hiddenimports` in `markdown_manager.spec`

**"Module not found"**
- Hidden import issue
- Check PyInstaller warnings during build

**"Slow startup"**
- Normal for first run
- Consider directory distribution for faster startup

**"Antivirus blocking"**
- Add exception for the executable
- Sign the executable (for professional distribution)

## 📊 Performance Considerations

### File Size Optimization
- **Base size**: ~150-200MB (includes Python runtime and all dependencies)
- **UPX compression**: Can reduce size by 30-50%
- **Exclude unused modules**: Remove unnecessary imports

### Startup Time
- **First run**: 15-30 seconds (extraction time)
- **Subsequent runs**: 5-10 seconds
- **Directory mode**: Faster startup, but multiple files

### Runtime Performance
- **CPU usage**: Similar to Python script
- **Memory usage**: Slightly higher due to bundled runtime
- **File I/O**: Same as Python script

## 🔄 Automated Building

### GitHub Actions (Continuous Integration)
The project includes GitHub Actions workflow for automated executable building:

```yaml
# .github/workflows/build-exe.yml
- name: Build Windows Executable
  run: python scripts/build_exe.py
  
- name: Upload Executable
  uses: actions/upload-artifact@v3
  with:
    name: MarkdownManager-Windows
    path: dist/MarkdownManager.exe
```

### Local Automation
```bash
# Add to Makefile
build-exe:
	python scripts/build_exe.py

# Build executable
make build-exe
```

## 📋 Distribution Checklist

Before distributing your executable:

- [ ] **Test on clean Windows system** (without Python installed)
- [ ] **Test with different Windows versions** (10, 11)
- [ ] **Include documentation** (README, .env.example)
- [ ] **Provide configuration guide** for Azure OpenAI setup
- [ ] **Consider code signing** for professional distribution
- [ ] **Create installer** (optional but recommended)
- [ ] **Test antivirus compatibility**
- [ ] **Verify all features work** (file upload, AI summarization, sync)

## 🆘 Troubleshooting

### Build Issues
```bash
# Clean build environment
rm -rf build/ dist/
python scripts/build_exe.py

# Verbose PyInstaller output
pyinstaller --log-level DEBUG markdown_manager.spec
```

### Runtime Issues
```bash
# Run with console output (for debugging)
# Ensure console=True in spec file
MarkdownManager.exe

# Check temp directory for extraction logs
echo %TEMP%
```

### Common Fixes
1. **Missing modules**: Add to `hiddenimports` in spec file
2. **Data files not found**: Add to `datas` in spec file  
3. **Slow performance**: Try directory distribution mode
4. **Large file size**: Remove unused dependencies

## 📚 Additional Resources

- **PyInstaller Documentation**: https://pyinstaller.readthedocs.io/
- **Windows Packaging**: https://docs.python.org/3/distutils/builtdist.html
- **Code Signing**: https://docs.microsoft.com/en-us/windows/security/identity-protection/
- **Installer Creation**: https://jrsoftware.org/isinfo.php (Inno Setup)

The executable provides a convenient way for users to run Markdown Manager without technical setup, making your application accessible to a broader audience! 🎉