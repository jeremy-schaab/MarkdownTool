# Markdown Manager Installation Guide

Multiple installation methods are available depending on your preference and technical comfort level.

## 🚀 Quick Installation Options

### Option 1: PowerShell Installer (Windows) - RECOMMENDED
**Easiest for Windows users** - Handles everything automatically including Python installation if needed.

1. **Download and run the installer:**
   ```powershell
   # Download the installer script
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/YOUR_USERNAME/MarkdownTool/main/install.ps1" -OutFile "install.ps1"
   
   # Run the installer
   PowerShell -ExecutionPolicy Bypass -File install.ps1
   ```

2. **Or download project and run locally:**
   ```powershell
   # If you have the project files locally
   PowerShell -ExecutionPolicy Bypass -File install.ps1
   ```

**What it does:**
- ✅ Checks for Python 3.8+ (installs if needed)
- ✅ Installs all dependencies automatically
- ✅ Creates .env configuration file
- ✅ Creates desktop shortcut
- ✅ Optionally starts the application

### Option 2: Batch File Installer (Windows)
**Simple batch file installer** - Requires Python to be pre-installed.

1. **Download and run:**
   ```batch
   # Download the project or navigate to project folder
   install.bat
   ```

**Prerequisites:**
- Python 3.8+ must be installed
- Internet connection for downloading dependencies

### Option 3: Manual Installation (All Platforms)
**Cross-platform manual setup** - Works on Windows, Mac, and Linux.

1. **Clone or download the project:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/MarkdownTool.git
   cd MarkdownTool
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   # Copy and edit the configuration file
   cp .env.example .env
   # Edit .env with your Azure OpenAI credentials
   ```

4. **Run the application:**
   ```bash
   python run_app.py
   ```

### Option 4: Pip Package (Future)
**Python package manager** - For distribution via PyPI.

```bash
# Once published to PyPI
pip install markdown-manager
markdown-manager
```

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space

### Python Dependencies
- `streamlit` - Web framework for the UI
- `markdown` - Markdown processing
- `pygments` - Syntax highlighting
- `streamlit-ace` - Code editor component
- `openai` - Azure OpenAI integration
- `python-dotenv` - Environment configuration

## 🔧 Configuration

### Azure OpenAI Setup (Required for AI Features)
1. **Get Azure OpenAI credentials:**
   - Create an Azure OpenAI resource
   - Deploy a GPT model (GPT-4 or GPT-3.5-turbo recommended)
   - Note your endpoint URL and API key

2. **Configure .env file:**
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_CHAT_DEPLOYMENT=your-deployment-name
   ```

### Optional Configuration
```env
AZURE_OPENAI_MAX_TOKENS=128000
AZURE_OPENAI_TEMPERATURE=1.0
AZURE_OPENAI_REQUEST_TIMEOUT=180
```

## 🎯 Usage

### Starting the Application
- **Desktop Shortcut**: Double-click "Markdown Manager" (if created by installer)
- **Command Line**: Run `python run_app.py` in the project directory
- **Direct Streamlit**: Run `streamlit run markdown_viewer.py --server.port 8501`

### First Time Setup
1. Open the application at http://localhost:8501
2. Browse to a folder containing markdown files
3. Select a markdown file to view
4. (Optional) Test AI summarization features

### Features Available
- 📄 **Markdown Viewing**: Syntax highlighted, properly formatted display
- ✏️ **Inline Editing**: Edit markdown with live preview
- 🤖 **AI Summaries**: Multiple template options including document improvement
- 🔗 **Link Navigation**: Click internal markdown links to navigate
- 💾 **File Management**: Save, download, and organize markdown files

## 🆘 Troubleshooting

### Common Issues

**"Python not found"**
- Install Python 3.8+ from https://python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**"Streamlit not found"**
- Run: `pip install streamlit`

**"AI features not working"**
- Check .env file configuration
- Verify Azure OpenAI credentials are correct
- Ensure your Azure OpenAI deployment is active

**"Port already in use"**
- Close existing instances or use different port:
  ```bash
  streamlit run markdown_viewer.py --server.port 8502
  ```

### Getting Help
- Check the README.md for detailed feature documentation
- Review the .env.example file for configuration examples
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## 📦 Distribution

### For Developers
To package for distribution:

1. **Create wheel package:**
   ```bash
   python setup.py bdist_wheel
   ```

2. **Install from wheel:**
   ```bash
   pip install dist/markdown_manager-1.0.0-py3-none-any.whl
   ```

3. **Upload to PyPI:**
   ```bash
   twine upload dist/*
   ```