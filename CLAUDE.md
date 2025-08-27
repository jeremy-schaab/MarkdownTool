# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based markdown file viewer application that allows users to browse and view markdown files with syntax highlighting and internal link navigation. The main application is in `markdown_viewer.py` with a simple Python runner script and Windows batch file for launching.

## Commands

### Running the Application
- `python run_app.py` - Start the Streamlit app on port 8501
- `run_app.bat` - Windows batch file to start the app
- `python -m streamlit run markdown_viewer.py --server.port 8501` - Direct Streamlit command

### Dependencies
- `pip install -r requirements.txt` - Install required packages (streamlit, markdown, pygments)

## Architecture

The application consists of a single main module with these key components:

### Core Functions
- `find_markdown_files()` - Recursively discovers .md/.markdown files in directories
- `render_markdown()` - Converts markdown to HTML with extensions (code highlighting, tables, TOC, etc.)
- `resolve_markdown_link()` - Resolves relative markdown links for internal navigation
- `main()` - Streamlit app entry point with sidebar file browser and main content area

### Key Features
- File upload and local folder browsing
- Session state management for file selection persistence
- HTML component with custom CSS for styled markdown rendering
- JavaScript-based internal link navigation system
- GitHub-style syntax highlighting with Pygments

### Navigation System
The app implements a complex internal link navigation system using:
- URL query parameters (`navigate_to`)
- JavaScript event handling in HTML components
- Multiple fallback communication methods between iframe and parent
- Session state updates for seamless file transitions

### Styling
Custom CSS provides GitHub-style formatting with syntax highlighting classes for code blocks, proper table styling, and responsive design elements.