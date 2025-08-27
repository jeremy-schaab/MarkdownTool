@echo off
echo Starting Markdown Viewer...
echo Open your browser and go to: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.
python -m streamlit run markdown_viewer.py --server.port 8501
pause