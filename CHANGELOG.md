# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Standalone executable support with PyInstaller
- .claude and .fyiai directory structure for AI workflow integration
- Enhanced gitignore for development artifacts

### Changed
- Updated documentation to reflect production-grade structure
- Improved CLI entry point with better error handling

## [1.2.0] - 2024-09-07

### Added
- Production-grade project structure with `src/` layout
- Comprehensive development tooling and CI/CD setup
- CLI entry point via `markdown-manager` command
- Configuration management system in `config/` directory
- Enhanced testing framework with pytest and fixtures
- Pre-commit hooks for code quality automation
- API documentation structure in `docs/`
- Contributing guidelines with development workflow
- Docker and Kubernetes support for containerized deployments
- Makefile for common development tasks
- Professional PyInstaller executable build system

### Changed
- Reorganized codebase into proper Python package structure under `src/markdown_manager/`
- Moved main application from `markdown_viewer.py` to `src/markdown_manager/app.py`
- Updated dependencies with version pinning in requirements files
- Improved error handling and logging throughout the application
- Enhanced documentation with comprehensive deployment guides
- Modernized build system using `pyproject.toml` instead of legacy `setup.py`

### Fixed
- Project structure for better maintainability and standards compliance
- Import paths after major restructuring
- Backward compatibility with existing user workflows
- Package discovery and installation issues

## [1.1.0] - 2024-09-05

### Added
- Azure Blob Storage synchronization feature
- Two-way sync (push/pull) capabilities
- Automatic container management
- Configuration persistence in `.fyiai/cloud/sync/config.json`
- Enhanced UI with cloud sync controls

### Changed
- Updated README with comprehensive Azure sync documentation
- Improved file organization for cloud features

### Fixed
- File path handling for cloud operations
- Error handling in sync operations

## [1.0.0] - 2024-08-29

### Added
- AI-powered document summarization using Azure OpenAI GPT-5 Mini
- 5 different summary templates (High Level, Detailed, Architectural, Technical Detail, Technical Review)
- Multiple display layouts for summaries (sidebar, side-by-side, tabbed)
- Smart file organization for AI summaries in `ai-summary/<analysis-name>/` folders
- Large document support (up to ~1 million characters)
- Metadata headers for generated summaries
- Environment-based configuration with `.env` file support
- Enhanced markdown editing with Streamlit-ACE editor
- Multiple editing modes (inline, side-by-side, tabbed)
- Formatting toolbar with quick-insert buttons
- Save/download functionality with confirmation dialogs
- Unsaved changes detection

### Changed
- Completely rewritten UI using Streamlit components
- Improved file navigation with session persistence
- Enhanced internal link resolution system
- Better error handling and user feedback
- Updated documentation with AI features

### Fixed
- Internal markdown link navigation
- File path resolution issues
- Session state management

## [0.3.0] - 2024-08-27

### Added
- Real-time markdown editing capabilities
- Live preview functionality
- File upload support
- GitHub-style CSS rendering
- Syntax highlighting for code blocks
- Table support with proper formatting

### Changed
- Improved UI layout and navigation
- Better file management system
- Enhanced markdown rendering engine

### Fixed
- File path handling on Windows systems
- Markdown parsing edge cases

## [0.2.0] - 2024-08-26

### Added
- Internal link navigation between markdown files
- Session state persistence
- Enhanced file browser with directory navigation
- Custom CSS styling for GitHub-like appearance

### Changed
- Improved file discovery algorithm
- Better error handling for missing files
- Enhanced user interface components

### Fixed
- File path resolution for relative links
- Browser refresh state management

## [0.1.0] - 2024-08-25

### Added
- Basic markdown file viewer
- Local folder browsing capability
- Streamlit-based web interface
- Support for .md and .markdown files
- Basic file upload functionality
- Simple navigation between files

### Features
- Recursive file discovery in directories
- Basic markdown to HTML conversion
- Simple file selection interface
- Port configuration (default 8501)

---

## Legend

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes