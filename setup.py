#!/usr/bin/env python3
"""
Setup script for Markdown Manager
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="markdown-manager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com", 
    description="A Streamlit-based markdown file viewer with AI-powered summarization and editing capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/MarkdownTool",
    packages=find_packages(),
    py_modules=['markdown_viewer', 'ai_service', 'run_app'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Markup",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        '': ['*.md', '*.txt', '*.example'],
    },
    entry_points={
        'console_scripts': [
            'markdown-manager=run_app:main',
        ],
    },
    keywords="markdown viewer editor ai summarization streamlit",
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/MarkdownTool/issues",
        "Source": "https://github.com/YOUR_USERNAME/MarkdownTool",
    },
)