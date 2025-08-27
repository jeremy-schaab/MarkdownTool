# User Guide

## Getting Started

Welcome to the Markdown Viewer! This application allows you to browse and view markdown files in a beautiful, formatted way.

### How to Use

1. Enter the path to your folder in the text input
2. Browse the list of markdown files in the sidebar
3. Click on any file to view its contents

### Supported Features

- [x] Recursive file discovery
- [x] Beautiful markdown rendering
- [x] Code syntax highlighting
- [x] Table formatting
- [x] Lists and blockquotes

### Tips

- Use the folder path input to navigate to different directories
- All `.md` and `.markdown` files will be discovered automatically
- Files are sorted alphabetically for easy browsing

## Technical Details

The app uses:
- **Streamlit** for the web interface
- **Python-Markdown** for rendering
- **Pygments** for code highlighting

```bash
# To run the app
streamlit run markdown_viewer.py
```