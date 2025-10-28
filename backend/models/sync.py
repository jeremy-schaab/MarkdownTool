"""Azure sync Pydantic models"""

from pydantic import BaseModel, Field
from typing import Optional


class SyncConfig(BaseModel):
    """Azure Blob Storage sync configuration"""
    project_root_folder: str = Field(..., description="Project root folder path")
    project_doc_folder: str = Field(..., description="Documentation folder path")
    azure_connection_string: str = Field(..., description="Azure Storage connection string")
    container_name: Optional[str] = Field("markdown-docs", description="Azure container name")


class SyncRequest(BaseModel):
    """Request to sync files with Azure"""
    config: SyncConfig = Field(..., description="Sync configuration")
    direction: str = Field(..., description="Sync direction: 'push' or 'pull'")


class SyncResponse(BaseModel):
    """Response from sync operation"""
    success: bool = Field(..., description="Whether sync was successful")
    message: str = Field(..., description="Status message")
    files_synced: int = Field(0, description="Number of files synced")
    bytes_transferred: Optional[int] = Field(None, description="Total bytes transferred")
    error: Optional[str] = Field(None, description="Error message if failed")


class SyncConfigSaveRequest(BaseModel):
    """Request to save sync configuration"""
    config: SyncConfig = Field(..., description="Configuration to save")


class SyncConfigLoadRequest(BaseModel):
    """Request to load sync configuration"""
    project_root: str = Field(..., description="Project root folder to load config from")
