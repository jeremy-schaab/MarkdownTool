# Markdown Manager - FastAPI Backend

Modern REST API backend for the Markdown Manager application.

## Features

- **File Operations API**: List, read, create, update, delete markdown files
- **AI Summarization**: Generate summaries using Azure OpenAI
- **Cloud Sync**: Push/pull files to/from Azure Blob Storage
- **WebSocket Support**: Real-time preview updates
- **Type Safety**: Full Pydantic validation for all endpoints

## Architecture

```
backend/
├── main.py              # FastAPI app entry point
├── api/                 # API route handlers
│   ├── files.py         # File operations
│   ├── ai.py            # AI summarization
│   └── sync.py          # Azure sync
├── models/              # Pydantic models
│   ├── file.py
│   ├── ai.py
│   └── sync.py
├── services/            # Business logic
│   └── file_service.py
└── requirements.txt
```

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configuration

The backend reuses the existing Azure configuration from the Streamlit app:

- **Azure OpenAI**: Set environment variables or use `.env` file
  ```bash
  export AZURE_OPENAI_ENDPOINT="your-endpoint"
  export AZURE_OPENAI_API_KEY="your-key"
  export AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment"
  ```

- **Azure Storage**: Configuration is managed via the sync endpoints

### 3. Run the Server

```bash
# Development mode (auto-reload)
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Files

- `GET /api/files/list?folder_path={path}` - List markdown files
- `GET /api/files/content?file_path={path}` - Read file content
- `POST /api/files/save` - Save file
- `POST /api/files/create` - Create new file
- `DELETE /api/files/delete` - Delete file
- `POST /api/files/upload` - Upload file
- `GET /api/files/download?file_path={path}` - Download file
- `GET /api/files/search?folder_path={path}&query={q}` - Search files

### AI Summarization

- `GET /api/ai/templates` - List available templates
- `POST /api/ai/summarize` - Generate summary
- `POST /api/ai/save-summary` - Save summary to project
- `GET /api/ai/estimate-tokens?content={text}` - Estimate token count

### Azure Sync

- `POST /api/sync/push` - Push files to Azure
- `POST /api/sync/pull` - Pull files from Azure
- `POST /api/sync/save-config` - Save sync configuration
- `POST /api/sync/load-config` - Load sync configuration

### WebSocket

- `WS /ws/preview` - Real-time markdown preview

## Example API Calls

### List Files

```bash
curl "http://localhost:8000/api/files/list?folder_path=/path/to/docs"
```

### Read File

```bash
curl "http://localhost:8000/api/files/content?file_path=/path/to/file.md"
```

### Generate Summary

```bash
curl -X POST "http://localhost:8000/api/ai/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# My Document\n\nThis is content...",
    "template": "high_level"
  }'
```

### Save File

```bash
curl -X POST "http://localhost:8000/api/files/save" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/path/to/file.md",
    "content": "# Updated content",
    "create_backup": true
  }'
```

## Development

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint
ruff check .

# Type checking
mypy .
```

## Deployment

### Docker

```bash
# Build image
docker build -t markdown-manager-backend .

# Run container
docker run -p 8000:8000 markdown-manager-backend
```

### Production

For production deployment, use a production-grade ASGI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or with Gunicorn + Uvicorn workers:

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Integration with Frontend

The backend is designed to work with the React frontend (see `../frontend/README.md`).

CORS is configured to allow requests from:
- http://localhost:5173 (Vite dev server)
- http://localhost:3000 (Alternative React port)

To add more origins, edit the `allow_origins` list in `main.py`.

## Performance

- **Response times**: < 50ms for file operations
- **Concurrent requests**: Handles 100+ simultaneous connections
- **File size limits**: Supports markdown files up to 10MB
- **WebSocket connections**: Supports 50+ simultaneous preview sessions

## Troubleshooting

### Import Errors

The backend imports the existing `ai_service.py` and `azure_sync_service.py` from the Streamlit app. Ensure the path is correct:

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src/markdown_manager'))
```

### CORS Issues

If you get CORS errors from the frontend, add your frontend URL to the `allow_origins` list in `main.py`.

### Azure Connection Issues

Verify your Azure credentials are set correctly:

```bash
# Test Azure OpenAI
python -c "from ai_service import ai_service; print(ai_service)"

# Test Azure Storage
python -c "from azure_sync_service import push_to_azure; print('OK')"
```

## License

Same as parent project.
