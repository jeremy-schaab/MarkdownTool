import { useState } from 'react';
import { File, Folder, FolderOpen, Search } from 'lucide-react';
import type { FileNode } from '../types';

interface FileBrowserProps {
  files: FileNode[];
  selectedFile: string | null;
  onFileSelect: (path: string) => void;
  isLoading?: boolean;
}

export function FileBrowser({ files, selectedFile, onFileSelect, isLoading }: FileBrowserProps) {
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());
  const [searchQuery, setSearchQuery] = useState('');

  const toggleFolder = (path: string) => {
    setExpandedFolders(prev => {
      const next = new Set(prev);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  };

  const filterFiles = (nodes: FileNode[], query: string): FileNode[] => {
    if (!query) return nodes;

    return nodes
      .map(node => {
        if (node.is_dir && node.children) {
          const filteredChildren = filterFiles(node.children, query);
          if (filteredChildren.length > 0) {
            return { ...node, children: filteredChildren };
          }
        }

        if (node.name.toLowerCase().includes(query.toLowerCase())) {
          return node;
        }

        return null;
      })
      .filter((node): node is FileNode => node !== null);
  };

  const renderNode = (node: FileNode, level: number = 0) => {
    const isExpanded = expandedFolders.has(node.path);
    const isSelected = selectedFile === node.path;

    if (node.is_dir) {
      return (
        <div key={node.path}>
          <div
            className={`flex items-center gap-2 px-3 py-1.5 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md transition-colors`}
            style={{ paddingLeft: `${level * 16 + 12}px` }}
            onClick={() => toggleFolder(node.path)}
          >
            {isExpanded ? (
              <FolderOpen className="w-4 h-4 text-blue-500" />
            ) : (
              <Folder className="w-4 h-4 text-blue-500" />
            )}
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {node.name}
            </span>
          </div>
          {isExpanded && node.children && (
            <div>
              {node.children.map(child => renderNode(child, level + 1))}
            </div>
          )}
        </div>
      );
    }

    return (
      <div
        key={node.path}
        className={`flex items-center gap-2 px-3 py-1.5 cursor-pointer rounded-md transition-colors ${
          isSelected
            ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
            : 'hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-700 dark:text-gray-300'
        }`}
        style={{ paddingLeft: `${level * 16 + 12}px` }}
        onClick={() => onFileSelect(node.path)}
      >
        <File className="w-4 h-4" />
        <span className="text-sm truncate">{node.name}</span>
      </div>
    );
  };

  const filteredFiles = filterFiles(files, searchQuery);

  return (
    <div className="h-full flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700">
      {/* Search */}
      <div className="p-3 border-b border-gray-200 dark:border-gray-700">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search files..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      {/* File Tree */}
      <div className="flex-1 overflow-y-auto p-2">
        {isLoading ? (
          <div className="flex items-center justify-center h-32 text-gray-500 dark:text-gray-400">
            Loading...
          </div>
        ) : filteredFiles.length === 0 ? (
          <div className="flex items-center justify-center h-32 text-gray-500 dark:text-gray-400 text-sm">
            {searchQuery ? 'No files found' : 'No markdown files'}
          </div>
        ) : (
          <div className="space-y-0.5">
            {filteredFiles.map(node => renderNode(node))}
          </div>
        )}
      </div>
    </div>
  );
}
