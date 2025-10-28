"""File operations service"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import logging

from models.file import FileItem, FileContent, FileListResponse

logger = logging.getLogger(__name__)


class FileService:
    """Service for file operations"""

    def __init__(self):
        self.markdown_extensions = ('.md', '.markdown')

    def list_markdown_files(
        self,
        folder_path: str,
        search_query: Optional[str] = None
    ) -> FileListResponse:
        """
        List all markdown files in a folder recursively.
        Returns a tree structure.
        """
        folder_path = Path(folder_path)

        if not folder_path.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")

        # Build file tree
        file_tree = self._build_file_tree(folder_path, search_query)

        # Count total markdown files
        total_count = self._count_markdown_files(folder_path)

        return FileListResponse(
            files=[file_tree] if file_tree else [],
            total_count=total_count,
            folder_path=str(folder_path)
        )

    def _build_file_tree(
        self,
        path: Path,
        search_query: Optional[str] = None
    ) -> Optional[FileItem]:
        """Recursively build file tree structure"""

        if not path.exists():
            return None

        # Get file/dir info
        stat = path.stat()

        if path.is_file():
            # Only include markdown files
            if not path.suffix.lower() in self.markdown_extensions:
                return None

            # Apply search filter
            if search_query and search_query.lower() not in path.name.lower():
                return None

            return FileItem(
                name=path.name,
                path=str(path),
                is_directory=False,
                size=stat.st_size,
                modified=datetime.fromtimestamp(stat.st_mtime)
            )

        elif path.is_dir():
            # Build children
            children = []
            try:
                for item in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                    child = self._build_file_tree(item, search_query)
                    if child:
                        children.append(child)
            except PermissionError:
                logger.warning(f"Permission denied: {path}")
                return None

            # Only include directories that have markdown files
            if not children:
                return None

            return FileItem(
                name=path.name,
                path=str(path),
                is_directory=True,
                size=None,
                modified=datetime.fromtimestamp(stat.st_mtime),
                children=children
            )

        return None

    def _count_markdown_files(self, folder_path: Path) -> int:
        """Count total markdown files recursively"""
        count = 0
        try:
            for item in folder_path.rglob("*"):
                if item.is_file() and item.suffix.lower() in self.markdown_extensions:
                    count += 1
        except PermissionError:
            pass
        return count

    def read_file(self, file_path: str) -> FileContent:
        """Read file content"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Read content
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        stat = path.stat()

        return FileContent(
            path=str(path),
            name=path.name,
            content=content,
            size=stat.st_size,
            modified=datetime.fromtimestamp(stat.st_mtime),
            is_temporary='.tmp' in path.name
        )

    def save_file(
        self,
        file_path: str,
        content: str,
        create_backup: bool = True
    ) -> dict:
        """Save content to file with optional backup"""
        path = Path(file_path)

        # Create backup if file exists and backup requested
        if path.exists() and create_backup:
            backup_path = path.with_suffix(path.suffix + '.bak')
            shutil.copy2(path, backup_path)
            logger.info(f"Backup created: {backup_path}")

        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"File saved: {path}")

        return {
            "success": True,
            "message": "File saved successfully",
            "path": str(path),
            "backup_created": create_backup and path.exists()
        }

    def delete_file(self, file_path: str) -> dict:
        """Delete a file"""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.is_dir():
            raise ValueError(f"Cannot delete directory: {file_path}")

        # Delete file
        path.unlink()
        logger.info(f"File deleted: {path}")

        return {
            "success": True,
            "message": "File deleted successfully",
            "path": str(path)
        }

    def create_file(
        self,
        folder_path: str,
        filename: str,
        content: str = ""
    ) -> dict:
        """Create a new file"""
        folder = Path(folder_path)
        file_path = folder / filename

        if file_path.exists():
            raise FileExistsError(f"File already exists: {file_path}")

        # Ensure folder exists
        folder.mkdir(parents=True, exist_ok=True)

        # Create file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"File created: {file_path}")

        return {
            "success": True,
            "message": "File created successfully",
            "path": str(file_path)
        }

    def search_files(
        self,
        folder_path: str,
        query: str,
        content_search: bool = False
    ) -> List[FileItem]:
        """Search for files by name or content"""
        folder = Path(folder_path)
        results = []

        if not folder.exists():
            return results

        query_lower = query.lower()

        for item in folder.rglob("*"):
            if not item.is_file():
                continue

            if not item.suffix.lower() in self.markdown_extensions:
                continue

            # Search by filename
            if query_lower in item.name.lower():
                stat = item.stat()
                results.append(FileItem(
                    name=item.name,
                    path=str(item),
                    is_directory=False,
                    size=stat.st_size,
                    modified=datetime.fromtimestamp(stat.st_mtime)
                ))
                continue

            # Search by content if requested
            if content_search:
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query_lower in content.lower():
                            stat = item.stat()
                            results.append(FileItem(
                                name=item.name,
                                path=str(item),
                                is_directory=False,
                                size=stat.st_size,
                                modified=datetime.fromtimestamp(stat.st_mtime)
                            ))
                except (UnicodeDecodeError, PermissionError):
                    pass

        return results
