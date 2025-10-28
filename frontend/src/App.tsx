import { useState, useEffect, useCallback } from 'react';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { Save, Download, FolderOpen, FileText } from 'lucide-react';
import { FileBrowser } from './components/FileBrowser';
import { MarkdownEditor } from './components/MarkdownEditor';
import { MarkdownPreview } from './components/MarkdownPreview';
import { Toolbar } from './components/Toolbar';
import { fileAPI } from './services/api';
import { markdownSnippets, debounce, downloadFile } from './utils/markdown';
import type { FileNode } from './types';

function App() {
  // State
  const [folderPath, setFolderPath] = useState('');
  const [files, setFiles] = useState<FileNode[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [fileContent, setFileContent] = useState('');
  const [originalContent, setOriginalContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [previewContent, setPreviewContent] = useState('');

  const hasUnsavedChanges = fileContent !== originalContent;

  // Debounced preview update
  const updatePreview = useCallback(
    debounce((content: string) => {
      setPreviewContent(content);
    }, 300),
    []
  );

  // Update preview when content changes
  useEffect(() => {
    updatePreview(fileContent);
  }, [fileContent, updatePreview]);

  // Load files from folder
  const loadFolder = async (path: string) => {
    if (!path) return;

    setIsLoading(true);
    try {
      const fileList = await fileAPI.list(path);
      setFiles(fileList);
      setFolderPath(path);
    } catch (error) {
      console.error('Error loading folder:', error);
      alert('Failed to load folder. Please check the path.');
    } finally {
      setIsLoading(false);
    }
  };

  // Load file content
  const loadFile = async (path: string) => {
    setIsLoading(true);
    try {
      const file = await fileAPI.read(path);
      setFileContent(file.content);
      setOriginalContent(file.content);
      setPreviewContent(file.content);
      setSelectedFile(path);
    } catch (error) {
      console.error('Error loading file:', error);
      alert('Failed to load file.');
    } finally {
      setIsLoading(false);
    }
  };

  // Save file
  const saveFile = async () => {
    if (!selectedFile) return;

    setIsSaving(true);
    try {
      await fileAPI.save({
        path: selectedFile,
        content: fileContent,
        create_backup: true,
      });
      setOriginalContent(fileContent);
      alert('File saved successfully!');
    } catch (error) {
      console.error('Error saving file:', error);
      alert('Failed to save file.');
    } finally {
      setIsSaving(false);
    }
  };

  // Download file
  const handleDownload = () => {
    if (!selectedFile) return;
    const filename = selectedFile.split('/').pop() || 'document.md';
    downloadFile(fileContent, filename);
  };

  // Handle toolbar insert
  const handleToolbarInsert = (type: string) => {
    const snippet = markdownSnippets[type as keyof typeof markdownSnippets];
    if (snippet && (window as any).markdownEditor) {
      (window as any).markdownEditor.insertAtCursor(snippet);
    }
  };

  // Handle folder selection
  const handleFolderSelect = () => {
    const path = prompt('Enter folder path:');
    if (path) {
      loadFolder(path);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <FileText className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
              Markdown Manager
            </h1>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleFolderSelect}
              className="flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-md transition-colors"
            >
              <FolderOpen className="w-4 h-4" />
              Open Folder
            </button>

            {selectedFile && (
              <>
                <button
                  onClick={saveFile}
                  disabled={!hasUnsavedChanges || isSaving}
                  className="flex items-center gap-2 px-3 py-2 text-sm bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white rounded-md transition-colors"
                >
                  <Save className="w-4 h-4" />
                  {isSaving ? 'Saving...' : hasUnsavedChanges ? 'Save*' : 'Save'}
                </button>

                <button
                  onClick={handleDownload}
                  className="flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-md transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download
                </button>
              </>
            )}
          </div>
        </div>

        {/* Folder path display */}
        {folderPath && (
          <div className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            <span className="font-medium">Folder:</span> {folderPath}
          </div>
        )}
      </header>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {!folderPath ? (
          /* Welcome Screen */
          <div className="h-full flex items-center justify-center">
            <div className="text-center">
              <FolderOpen className="w-16 h-16 mx-auto mb-4 text-gray-400" />
              <h2 className="text-2xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
                Welcome to Markdown Manager
              </h2>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Open a folder to get started
              </p>
              <button
                onClick={handleFolderSelect}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
              >
                Open Folder
              </button>
            </div>
          </div>
        ) : (
          /* Split View */
          <PanelGroup direction="horizontal">
            {/* File Browser */}
            <Panel defaultSize={20} minSize={15} maxSize={40}>
              <FileBrowser
                files={files}
                selectedFile={selectedFile}
                onFileSelect={loadFile}
                isLoading={isLoading}
              />
            </Panel>

            <PanelResizeHandle className="w-1 bg-gray-300 dark:bg-gray-700 hover:bg-blue-500 transition-colors" />

            {/* Editor & Preview */}
            <Panel defaultSize={80} minSize={30}>
              {selectedFile ? (
                <div className="h-full flex flex-col">
                  {/* Toolbar */}
                  <Toolbar onInsert={handleToolbarInsert} />

                  {/* Editor & Preview Split */}
                  <div className="flex-1 overflow-hidden">
                    <PanelGroup direction="horizontal">
                      <Panel defaultSize={50} minSize={30}>
                        <MarkdownEditor
                          value={fileContent}
                          onChange={(value) => setFileContent(value || '')}
                        />
                      </Panel>

                      <PanelResizeHandle className="w-1 bg-gray-300 dark:bg-gray-700 hover:bg-blue-500 transition-colors" />

                      <Panel defaultSize={50} minSize={30}>
                        <MarkdownPreview content={previewContent} />
                      </Panel>
                    </PanelGroup>
                  </div>
                </div>
              ) : (
                /* No file selected */
                <div className="h-full flex items-center justify-center bg-white dark:bg-gray-900">
                  <div className="text-center text-gray-500 dark:text-gray-400">
                    <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
                    <p>Select a file to edit</p>
                  </div>
                </div>
              )}
            </Panel>
          </PanelGroup>
        )}
      </div>
    </div>
  );
}

export default App;
