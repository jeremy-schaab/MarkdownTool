# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a production-grade Streamlit-based markdown file manager with viewer, editor, and AI-powered summarization capabilities. The application allows users to browse local folders, edit markdown files with real-time preview, sync with Azure Blob Storage, and generate intelligent summaries using Azure OpenAI. The main application is now structured as a proper Python package in `src/markdown_manager/` with CLI entry points, comprehensive testing, and deployment support.

## Commands

### Running the Application (Production)
- `markdown-manager` - CLI entry point (after `pip install -e .`)
- `python src/markdown_manager/cli.py` - Direct CLI execution
- `python -m streamlit run src/markdown_manager/app.py --server.port 8501` - Direct Streamlit command

### Legacy Support
- `python run_app.py` - Legacy runner (backward compatibility)
- `run_app.bat` - Windows batch file to start the app

### Development Commands
- `make install-dev` - Install with development dependencies
- `make test` - Run pytest test suite
- `make lint` - Run code linting (ruff, black)
- `make format` - Format code with black and ruff
- `make run-dev` - Run in development mode
- `pre-commit run --all-files` - Run pre-commit hooks

### Dependencies
- `pip install -e .` - Install package in editable mode (recommended)
- `pip install -r requirements.txt` - Install production requirements
- `pip install -r requirements-dev.txt` - Install development requirements

## Architecture

The application follows a modern Python package structure with these key components:

### Package Structure
- `src/markdown_manager/` - Main application package
  - `app.py` - Main Streamlit application (formerly markdown_viewer.py)
  - `ai_service.py` - Azure OpenAI integration for AI summarization
  - `azure_sync_service.py` - Azure Blob Storage synchronization
  - `cli.py` - Command-line interface entry point
- `tests/` - Comprehensive test suite with pytest
- `config/` - Configuration management system
- `docs/` - Documentation and guides
- `deployment/` - Docker and Kubernetes configurations

### Core Functions (app.py)
- `find_markdown_files()` - Recursively discovers .md/.markdown files in directories
- `render_markdown()` - Converts markdown to HTML with extensions (code highlighting, tables, TOC, etc.)
- `resolve_markdown_link()` - Resolves relative markdown links for internal navigation
- `main()` - Streamlit app entry point with sidebar file browser and main content area

### Key Features
- **File Management**: Upload, browse, edit with real-time preview
- **AI Integration**: GPT-5 Mini summarization with multiple templates
- **Cloud Sync**: Azure Blob Storage two-way synchronization
- **Rich Editor**: Streamlit-ACE editor with formatting toolbar
- **Navigation**: Complex internal link system with JavaScript fallbacks
- **Production Ready**: CLI entry points, comprehensive testing, deployment configs

### Services Architecture
- `ai_service.py` - Handles Azure OpenAI API communication, token estimation, and summary generation
- `azure_sync_service.py` - Manages cloud synchronization, container operations, and file transfers
- `cli.py` - Provides command-line interface with Click framework

### Testing & Quality
- Pytest test suite with fixtures and mocking
- Pre-commit hooks for code quality (black, ruff, mypy)
- GitHub Actions CI/CD pipeline
- Docker containerization support

### Navigation System
The app implements a complex internal link navigation system using:
- URL query parameters (`navigate_to`)
- JavaScript event handling in HTML components
- Multiple fallback communication methods between iframe and parent
- Session state updates for seamless file transitions

### Styling
Custom CSS provides GitHub-style formatting with syntax highlighting classes for code blocks, proper table styling, and responsive design elements.