"""File operations API endpoints"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse
from typing import Optional
import os
import logging
from pathlib import Path

from models.file import (
    FileListResponse,
    FileContent,
    FileSaveRequest,
    FileDeleteRequest,
    FileUploadRequest,
    FileItem
)
from services.file_service import FileService

router = APIRouter()
logger = logging.getLogger(__name__)
file_service = FileService()


@router.get("/list", response_model=FileListResponse)
async def list_files(
    folder_path: str = Query(..., description="Folder path to scan"),
    search: Optional[str] = Query(None, description="Search filter")
):
    """
    List all markdown files in a folder recursively.
    Returns a tree structure of files and directories.
    """
    try:
        if not os.path.exists(folder_path):
            raise HTTPException(status_code=404, detail=f"Folder not found: {folder_path}")

        if not os.path.isdir(folder_path):
            raise HTTPException(status_code=400, detail=f"Path is not a directory: {folder_path}")

        result = file_service.list_markdown_files(folder_path, search_query=search)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/content", response_model=FileContent)
async def get_file_content(file_path: str = Query(..., description="File path to read")):
    """
    Read and return the content of a markdown file.
    """
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

        if not file_path.lower().endswith(('.md', '.markdown')):
            raise HTTPException(status_code=400, detail="File must be a markdown file")

        content = file_service.read_file(file_path)
        return content

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
async def save_file(request: FileSaveRequest):
    """
    Save content to a markdown file.
    Creates a backup if requested.
    """
    try:
        result = file_service.save_file(
            request.path,
            request.content,
            create_backup=request.create_backup
        )

        return result

    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete")
async def delete_file(request: FileDeleteRequest):
    """
    Delete a markdown file.
    Requires confirmation flag.
    """
    try:
        if not request.confirm:
            raise HTTPException(
                status_code=400,
                detail="Deletion requires confirmation. Set 'confirm' to true."
            )

        result = file_service.delete_file(request.path)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
async def create_file(request: FileUploadRequest):
    """
    Create a new markdown file.
    """
    try:
        result = file_service.create_file(
            request.folder_path,
            request.filename,
            request.content
        )

        return result

    except Exception as e:
        logger.error(f"Error creating file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_file(
    folder_path: str = Query(..., description="Destination folder"),
    file: UploadFile = File(...)
):
    """
    Upload a markdown file.
    """
    try:
        if not file.filename.lower().endswith(('.md', '.markdown')):
            raise HTTPException(
                status_code=400,
                detail="Only markdown files (.md, .markdown) are allowed"
            )

        content = await file.read()
        content_str = content.decode('utf-8')

        result = file_service.create_file(
            folder_path,
            file.filename,
            content_str
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download")
async def download_file(file_path: str = Query(..., description="File path to download")):
    """
    Download a markdown file.
    """
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type='text/markdown'
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_files(
    folder_path: str = Query(..., description="Folder to search in"),
    query: str = Query(..., description="Search query"),
    content_search: bool = Query(False, description="Search file contents (not just names)")
):
    """
    Search for markdown files by name or content.
    """
    try:
        results = file_service.search_files(folder_path, query, content_search)
        return {"results": results, "query": query, "count": len(results)}

    except Exception as e:
        logger.error(f"Error searching files: {e}")
        raise HTTPException(status_code=500, detail=str(e))
