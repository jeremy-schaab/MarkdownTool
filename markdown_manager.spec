# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Markdown Manager
This file defines how to build the Windows executable.
"""

import os
import sys
from pathlib import Path

# Get project root
project_root = Path().absolute()

# Add source directory to Python path
sys.path.insert(0, str(project_root / "src"))

block_cipher = None

# Define the main entry point
a = Analysis(
    ['src\\markdown_manager\\cli.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Include all necessary data files
        ('src\\markdown_manager\\*.py', 'markdown_manager'),
        ('.env.example', '.'),
        ('README.md', '.'),
        ('CHANGELOG.md', '.'),
        # Include test files for demo purposes
        ('test_files', 'test_files'),
        # Include config
        ('config', 'config'),
    ],
    hiddenimports=[
        # Streamlit dependencies
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.runtime.state',
        'streamlit_ace',
        
        # Markdown and syntax highlighting
        'markdown',
        'pygments',
        'pygments.lexers',
        'pygments.formatters',
        
        # AI and Azure services
        'openai',
        'azure.storage.blob',
        'azure.core',
        
        # Other dependencies
        'python_dotenv',
        'reportlab',
        'markdown2',
        'requests',
        'click',
        
        # Standard library modules that might be missed
        'email.mime.multipart',
        'email.mime.text',
        'email.mime.base',
        'json',
        'logging',
        'pathlib',
        'tempfile',
        'shutil',
        'subprocess',
        'threading',
        'queue',
        'urllib.parse',
        'urllib.request',
        'urllib.error',
        
        # Streamlit internal modules
        'streamlit.components.v1',
        'streamlit.delta_generator',
        'streamlit.runtime.metrics_util',
        'streamlit.runtime.legacy_caching',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude test and development modules
        'pytest',
        'black',
        'isort',
        'flake8',
        'mypy',
        'bandit',
        'pre_commit',
        'setuptools',
        'pip',
        'wheel',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate entries
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MarkdownManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False for windowed app, True for console app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',  # We'll create this file
    icon='assets\\icon.ico',  # We'll create this too
)