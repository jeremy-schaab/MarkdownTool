"""
FastAPI backend for Markdown Manager
Provides REST API for file operations, AI summarization, and cloud sync
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

# Import routers
from api import files, ai, sync

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for FastAPI app"""
    logger.info("Starting Markdown Manager Backend...")
    yield
    logger.info("Shutting down Markdown Manager Backend...")


# Create FastAPI app
app = FastAPI(
    title="Markdown Manager API",
    description="Backend API for markdown file management with AI summarization",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative React dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(sync.router, prefix="/api/sync", tags=["sync"])


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "name": "Markdown Manager API",
        "version": "2.0.0",
        "status": "healthy",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# WebSocket for real-time preview updates
active_connections: list[WebSocket] = []


@app.websocket("/ws/preview")
async def preview_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time markdown preview"""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info("Client connected to preview WebSocket")

    try:
        while True:
            # Receive markdown content from client
            data = await websocket.receive_json()

            # Echo back (in production, you might process/render here)
            await websocket.send_json({
                "type": "preview",
                "content": data.get("content", "")
            })

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("Client disconnected from preview WebSocket")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
