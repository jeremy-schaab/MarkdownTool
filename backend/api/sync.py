"""Azure Blob Storage sync API endpoints"""

from fastapi import APIRouter, HTTPException
import logging
import sys
import os
import json
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src/markdown_manager'))

from models.sync import (
    SyncConfig,
    SyncRequest,
    SyncResponse,
    SyncConfigSaveRequest,
    SyncConfigLoadRequest
)

router = APIRouter()
logger = logging.getLogger(__name__)

# Import sync service from existing codebase
try:
    from azure_sync_service import push_to_azure, pull_from_azure
except ImportError:
    logger.warning("Could not import azure_sync_service from existing codebase")
    push_to_azure = None
    pull_from_azure = None


@router.post("/push", response_model=SyncResponse)
async def push_files(request: SyncRequest):
    """
    Push (upload) files from local to Azure Blob Storage.
    """
    try:
        if not push_to_azure:
            raise HTTPException(
                status_code=503,
                detail="Azure sync service not available"
            )

        if request.direction != "push":
            raise HTTPException(
                status_code=400,
                detail="Invalid direction for push endpoint. Use 'push'."
            )

        # Perform push operation
        files_synced = 0
        try:
            # Call existing push_to_azure function
            push_to_azure(
                connection_string=request.config.azure_connection_string,
                project_root=request.config.project_root_folder,
                doc_folder=request.config.project_doc_folder,
                container_name=request.config.container_name or "markdown-docs"
            )

            # Count files (simplified)
            files_synced = _count_markdown_files(request.config.project_doc_folder)

            return SyncResponse(
                success=True,
                message=f"Successfully pushed {files_synced} files to Azure",
                files_synced=files_synced
            )

        except Exception as e:
            logger.error(f"Push failed: {e}")
            return SyncResponse(
                success=False,
                message="Push failed",
                files_synced=0,
                error=str(e)
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in push operation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pull", response_model=SyncResponse)
async def pull_files(request: SyncRequest):
    """
    Pull (download) files from Azure Blob Storage to local.
    """
    try:
        if not pull_from_azure:
            raise HTTPException(
                status_code=503,
                detail="Azure sync service not available"
            )

        if request.direction != "pull":
            raise HTTPException(
                status_code=400,
                detail="Invalid direction for pull endpoint. Use 'pull'."
            )

        # Perform pull operation
        files_synced = 0
        try:
            # Call existing pull_from_azure function
            pull_from_azure(
                connection_string=request.config.azure_connection_string,
                project_root=request.config.project_root_folder,
                doc_folder=request.config.project_doc_folder,
                container_name=request.config.container_name or "markdown-docs"
            )

            # Count files (simplified)
            files_synced = _count_markdown_files(request.config.project_doc_folder)

            return SyncResponse(
                success=True,
                message=f"Successfully pulled {files_synced} files from Azure",
                files_synced=files_synced
            )

        except Exception as e:
            logger.error(f"Pull failed: {e}")
            return SyncResponse(
                success=False,
                message="Pull failed",
                files_synced=0,
                error=str(e)
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in pull operation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save-config")
async def save_config(request: SyncConfigSaveRequest):
    """
    Save sync configuration to project's .fyiai folder.
    """
    try:
        config_dir = Path(request.config.project_root_folder) / ".fyiai" / "cloud" / "sync"
        config_path = config_dir / "config.json"

        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)

        # Save config
        config_data = {
            "project_root_folder": request.config.project_root_folder,
            "project_doc_folder": request.config.project_doc_folder,
            "azure_connection_string": request.config.azure_connection_string,
            "container_name": request.config.container_name
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4)

        return {
            "success": True,
            "message": f"Configuration saved to {config_path}",
            "path": str(config_path)
        }

    except Exception as e:
        logger.error(f"Error saving config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/load-config", response_model=SyncConfig)
async def load_config(request: SyncConfigLoadRequest):
    """
    Load sync configuration from project's .fyiai folder.
    """
    try:
        config_path = Path(request.project_root) / ".fyiai" / "cloud" / "sync" / "config.json"

        if not config_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Configuration not found at {config_path}"
            )

        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)

        return SyncConfig(**config_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def _count_markdown_files(folder_path: str) -> int:
    """Helper function to count markdown files"""
    try:
        count = 0
        for root, dirs, files in os.walk(folder_path):
            count += len([f for f in files if f.lower().endswith(('.md', '.markdown'))])
        return count
    except:
        return 0
