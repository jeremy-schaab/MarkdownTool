# 📄 Markdown Viewer & Editor

A powerful, web-based markdown file viewer and editor built with Streamlit. Browse local folders, upload files, and edit markdown documents with real-time preview and syntax highlighting.

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

## 🔧 Configuration

### Custom Port
To run on a different port:
```bash
python -m streamlit run markdown_viewer.py --server.port 8502
```

### File Permissions
The application requires read access to browse local folders and write access to save files directly. Uploaded files are handled through temporary storage.

## 🛡️ Security Features

- **Confirmation Dialogs**: Direct file saves require user confirmation to prevent accidental overwrites
- **Temporary File Protection**: Uploaded files cannot be directly overwritten (download-only)
- **Path Validation**: Internal link navigation validates file paths and extensions
- **Safe Rendering**: HTML content is safely rendered with Streamlit's built-in protections

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