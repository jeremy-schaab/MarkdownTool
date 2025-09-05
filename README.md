# 📄 Markdown Viewer, Editor & AI Summarizer

A powerful, web-based markdown file viewer, editor, and AI-powered summarization tool built with Streamlit. Browse local folders, upload files, edit markdown documents with real-time preview, and generate intelligent summaries using GPT-5 Mini.

## ✨ Features

### File Management
- **Local Folder Browsing**: Navigate and view markdown files from your local file system
- **File Upload**: Upload `.md` or `.markdown` files directly to the viewer
- **Internal Link Navigation**: Click on relative markdown links to navigate between files seamlessly

### Markdown Editing
- **Rich Text Editor**: Full-featured markdown editor with syntax highlighting
- **Multiple Layout Options**: Choose from inline, side-by-side, or tabbed editing modes
- **Live Preview**: Real-time markdown rendering with GitHub-style formatting
- **Formatting Toolbar**: Quick access buttons for common markdown elements (bold, italic, headers, links, code)

### Save & Export
- **Direct File Save**: Save changes directly back to the original file (with confirmation dialog)
- **Download Option**: Export modified files as downloads
- **Unsaved Changes Detection**: Visual indicators for modified content
- **Auto-backup**: Preserves original content for comparison

### ☁️ Cloud Sync with Azure Blob Storage
- **Two-Way Sync**: Push local changes to an Azure Blob Storage container or pull remote changes to your local machine.
- **Easy Configuration**: Set your Project Root and paste your Azure Connection String in the sidebar.
- **Automatic Container Management**: A container named `fyiai-{project-name}` is automatically used (and created if it doesn't exist).
- **Preserves Folder Structure**: The sync process maintains the relative directory structure of your files.
- **Configuration File**: Settings are stored in `.fyiai/cloud/sync/config.json` within your project root, making it easy to share or back up.

### AI-Powered Summarization 🤖
- **GPT-5 Mini Integration**: Generate intelligent summaries using Azure OpenAI's GPT-5 Mini model
- **5 Summary Templates**: Choose from High Level, Detailed Overview, Architectural, Technical Detail, or Technical Review perspectives
- **Multiple Display Layouts**: View summaries in sidebar, side-by-side, or tabbed layouts
- **Project Integration**: Summaries are saved to `ai-summary/<analysis-name>/` in your project directory
- **Large Document Support**: Process documents up to ~1 million characters with 128k token output capacity
- **Smart File Organization**: Auto-generated filenames with metadata headers for easy tracking

### Advanced Features
- **Syntax Highlighting**: Code blocks rendered with Pygments for multiple languages
- **Table Support**: Full markdown table rendering and editing
- **Table of Contents**: Automatic TOC generation for documents
- **Responsive Design**: Works on desktop and mobile devices
- **Session Persistence**: Remembers your last selected file and folder

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/jeremy-schaab/MarkdownTool.git
   cd MarkdownTool
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run_app.py
   ```
   
   Or run directly with Streamlit:
   ```bash
   python -m streamlit run markdown_viewer.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

### Alternative Installation Methods

#### Using Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv markdown-viewer-env

# Activate virtual environment
# On Windows:
markdown-viewer-env\Scripts\activate
# On macOS/Linux:
source markdown-viewer-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_app.py
```

#### Using Windows Batch File
For Windows users, you can use the provided batch file:
```bash
run_app.bat
```

## 📋 Requirements

The application requires the following Python packages:

- `streamlit` - Web framework for the user interface
- `markdown` - Markdown parsing and rendering
- `pygments` - Syntax highlighting for code blocks
- `streamlit-ace` - Code editor component for markdown editing
- `openai` - Azure OpenAI integration for AI summarization
- `python-dotenv` - Environment variable management for secure configuration
- `azure-storage-blob` - Client library for Azure Blob Storage synchronization

Full requirements are listed in `requirements.txt`.

## 🎯 Usage

### Getting Started

1. **Launch the application** using one of the installation methods above
2. **Browse local files** by entering a folder path in the sidebar
3. **Upload files** using the file uploader for quick access
4. **Select a markdown file** from the file list to view its contents

### Editing Files

1. **Enter Edit Mode**: Click the "✏️ Edit File" button in the sidebar
2. **Choose Layout**: Select from inline, side-by-side, or tabbed editing modes
3. **Edit Content**: Use the rich text editor with syntax highlighting
4. **Use Toolbar**: Click formatting buttons for quick markdown insertion
5. **Preview Changes**: View live preview (in side-by-side or tabbed modes)
6. **Save Changes**: Choose between "💾 Save File" (direct overwrite) or "📥 Download" (export copy)

### Navigation

- **Internal Links**: Click on relative markdown links (e.g., `[link](./other-file.md)`) to navigate between files
- **Folder Navigation**: Change the folder path to browse different directories
- **File History**: The app remembers your last selected file when refreshing

### Editing Modes

#### Inline Mode
- Full-screen editor for focused writing
- Minimal distractions, maximum editing space

#### Side-by-Side Mode
- Editor on the left, live preview on the right
- Real-time preview updates as you type

#### Tabbed Mode
- Switch between "Editor" and "Preview" tabs
- Clean interface with easy mode switching

### AI Summarization 🤖

#### Setup (Required for AI Features)
1. **Create `.env` file** in the project root with your Azure OpenAI credentials:
   ```env
   AZURE_OPENAI_ENDPOINT=your-endpoint-url
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-5-mini
   AZURE_OPENAI_MAX_TOKENS=128000
   AZURE_OPENAI_TEMPERATURE=0.25
   AZURE_OPENAI_REQUEST_TIMEOUT=180
   ```

#### Using AI Summarization
1. **Select a markdown file** to view its content
2. **Choose summary type** from 5 available templates:
   - **High Level Summary**: Brief overview with main topics and key points
   - **Detailed Overview**: Comprehensive analysis with context and implications
   - **Architectural Overview**: Focus on system design, components, and relationships
   - **Technical Detail**: Deep dive into implementation details and specifications
   - **Technical Review**: Critical analysis with strengths, weaknesses, and recommendations

3. **Select display layout**:
   - **Sidebar**: Summary appears in the sidebar (default)
   - **Side-by-Side**: Document on left, summary on right
   - **Tabbed**: Separate tabs for document and summary

4. **Generate Summary**: Click "✨ Generate Summary" button
5. **Save to Project**: Click "💾 Save to Project" to save directly to `ai-summary/<analysis-name>/` folder

#### AI Summary Features
- **Large Document Support**: Process files up to ~1 million characters
- **Smart File Naming**: `[filename]_[template]_summary.md`
- **Metadata Headers**: Include generation timestamp, template used, and source file
- **Project Organization**: Summaries saved to `YourProject/ai-summary/<analysis-name>/` folder
- **Multiple Templates**: Generate different perspectives of the same document

#### Example Workflow for Product Briefs
```
1. Set folder path to your project directory
2. Select product brief markdown file
3. Generate "High Level Summary" for stakeholders
4. Generate "Technical Review" for development team
5. Both summaries automatically saved to `ai-summary/<analysis-name>/` folder
6. Access organized summaries anytime from your project
```

## 🔧 Configuration

### Custom Port
To run on a different port:
```bash
python -m streamlit run markdown_viewer.py --server.port 8502
```

### Azure OpenAI Configuration
For AI summarization features, configure your Azure OpenAI credentials:

1. **Create `.env` file** in the project root
2. **Add your credentials**:
   ```env
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-5-mini
   ```
3. **Restart the application** to load the new configuration

### File Permissions
The application requires:
- **Read access** to browse local folders
- **Write access** to save files directly and create `ai-summary` folders
- **Network access** for Azure OpenAI API calls (if using AI features)

Uploaded files are handled through temporary storage.

## 🧪 Testing & Demo

### Live Demo
You can test the application with sample files:

1. **Clone the repository** and follow installation steps above
2. **Use the `test_files/` directory** included in the repository:
   ```
   test_files/
   ├── README.md          # Basic markdown with links
   ├── api_test.md        # API documentation example
   ├── guide.md           # User guide with complex formatting
   ├── links_test.md      # Internal link navigation test
   └── subfolder/
       └── notes.md       # Nested file for link testing
   ```

3. **Set folder path** to the `test_files` directory
4. **Try different features**:
   - Select files to view and edit
   - Test internal link navigation
   - Generate AI summaries (requires Azure OpenAI setup)
   - Try different layout modes

### Testing AI Features
To test AI summarization:
1. **Set up Azure OpenAI credentials** in `.env` file
2. **Select a test file** (e.g., `guide.md` for comprehensive content)
3. **Generate summaries** with different templates
4. **Check `test_files/ai-summary/`** folder for saved summaries

### Performance Testing
- **Large files**: Test with documents up to 1MB for AI processing
- **Multiple summaries**: Generate different template summaries for the same document
- **Layout switching**: Test all 3 display layouts (sidebar, side-by-side, tabbed)

## 🛡️ Security Features

- **Confirmation Dialogs**: Direct file saves require user confirmation to prevent accidental overwrites
- **Temporary File Protection**: Uploaded files cannot be directly overwritten (download-only)  
- **Path Validation**: Internal link navigation validates file paths and extensions
- **Safe Rendering**: HTML content is safely rendered with Streamlit's built-in protections
- **Secure Credentials**: Azure OpenAI credentials stored in `.env` file (not committed to git)
- **API Rate Limiting**: Built-in retry logic with exponential backoff for API calls

## 🎨 Customization

The application uses GitHub-style CSS for markdown rendering. The styling includes:

- Syntax highlighted code blocks
- Responsive tables
- Clean typography
- Mobile-friendly design

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```
Port 8501 is already in use
```
Solution: Use a different port or kill the existing process:
```bash
python -m streamlit run markdown_viewer.py --server.port 8502
```

**Module Not Found**
```
ModuleNotFoundError: No module named 'streamlit'
```
Solution: Install requirements:
```bash
pip install -r requirements.txt
```

**File Permission Errors**
```
PermissionError: [Errno 13] Permission denied
```
Solution: Ensure the application has read/write permissions for the target directory.

**AI Service Not Configured**
```
⚠️ AI service not configured. Please check your Azure OpenAI credentials in .env file.
```
Solution: Create `.env` file with proper Azure OpenAI credentials:
```env
AZURE_OPENAI_ENDPOINT=your-endpoint
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-5-mini
```

**Content Too Large**
```
Content is too large (XXX,XXX estimated tokens). Maximum allowed is XXX,XXX tokens.
```
Solution: Split large documents into smaller sections, or the document exceeds GPT-5 Mini's context window.

**API Rate Limits**
If you encounter rate limiting errors, the application will automatically retry with exponential backoff. For persistent issues, consider upgrading your Azure OpenAI tier.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the repository for license details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Markdown parsing by [Python-Markdown](https://python-markdown.github.io/)
- Syntax highlighting by [Pygments](https://pygments.org/)
- Code editor by [Streamlit-Ace](https://github.com/okld/streamlit-ace)

## 📧 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/jeremy-schaab/MarkdownTool/issues) on GitHub.

---

Made with ❤️ for the markdown community
