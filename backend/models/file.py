"""File-related Pydantic models"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class FileItem(BaseModel):
    """Represents a file or directory in the file tree"""
    name: str = Field(..., description="File or directory name")
    path: str = Field(..., description="Full path to file/directory")
    is_directory: bool = Field(..., description="Whether this is a directory")
    size: Optional[int] = Field(None, description="File size in bytes")
    modified: Optional[datetime] = Field(None, description="Last modified timestamp")
    children: Optional[List['FileItem']] = Field(None, description="Child items for directories")


# Enable forward references
FileItem.model_rebuild()


class FileListResponse(BaseModel):
    """Response for file listing"""
    files: List[FileItem] = Field(..., description="List of files and directories")
    total_count: int = Field(..., description="Total number of markdown files found")
    folder_path: str = Field(..., description="Root folder path")


class FileContent(BaseModel):
    """File content response"""
    path: str = Field(..., description="File path")
    name: str = Field(..., description="File name")
    content: str = Field(..., description="File content")
    size: int = Field(..., description="File size in bytes")
    modified: datetime = Field(..., description="Last modified timestamp")
    is_temporary: bool = Field(False, description="Whether this is a temporary file")


class FileSaveRequest(BaseModel):
    """Request to save file content"""
    path: str = Field(..., description="File path to save to")
    content: str = Field(..., description="New file content")
    create_backup: bool = Field(True, description="Whether to create a backup before saving")


class FileDeleteRequest(BaseModel):
    """Request to delete a file"""
    path: str = Field(..., description="File path to delete")
    confirm: bool = Field(False, description="Confirmation flag")


class FileUploadRequest(BaseModel):
    """Request to upload/create a new file"""
    folder_path: str = Field(..., description="Folder to create file in")
    filename: str = Field(..., description="New file name")
    content: str = Field("", description="Initial file content")
