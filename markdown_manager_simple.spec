# -*- mode: python ; coding: utf-8 -*-
"""
Simplified PyInstaller spec file for Markdown Manager
"""

import os
import sys
from pathlib import Path

# Get project root
project_root = Path().absolute()

# Add source directory to Python path
sys.path.insert(0, str(project_root / "src"))

block_cipher = None

# Only include essential hidden imports
a = Analysis(
    ['src\\markdown_manager\\cli.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # Essential data files only
        ('.env.example', '.'),
        ('README.md', '.'),
        ('test_files', 'test_files'),
    ],
    hiddenimports=[
        # Core Streamlit
        'streamlit',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.script_runner',
        'streamlit.components.v1',
        
        # Essential modules
        'markdown',
        'pygments',
        'streamlit_ace',
        'openai',
        'python_dotenv',
        'azure.storage.blob',
        'requests',
        'click',
        
        # Standard library essentials
        'subprocess',
        'pathlib',
        'json',
        'logging',
        'tempfile',
        'shutil',
        'urllib.parse',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude heavy packages we don't need
        'matplotlib',
        'pandas',
        'numpy',
        'scipy',
        'plotly',
        'jupyter',
        'IPython',
        'pyarrow',
        'numba',
        'llvmlite',
        'pygame',
        'PIL.ImageQt',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'tkinter',
        'test',
        'unittest',
        'doctest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

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
    upx=False,  # Disable UPX for faster build
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\icon.ico',
)