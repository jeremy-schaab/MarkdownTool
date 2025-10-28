// File types
export interface FileNode {
  name: string;
  path: string;
  is_dir: boolean;
  children?: FileNode[];
}

export interface FileContent {
  path: string;
  content: string;
  size: number;
  modified: string;
}

export interface SaveFileRequest {
  path: string;
  content: string;
  create_backup?: boolean;
}

export interface CreateFileRequest {
  folder_path: string;
  filename: string;
  content?: string;
}

// AI types
export interface AISummaryTemplate {
  id: string;
  name: string;
  description: string;
}

export interface AISummaryRequest {
  content: string;
  template: string;
  custom_prompt?: string;
}

export interface AISummaryResponse {
  summary: string;
  tokens_used: number;
  template_used: string;
}

// Sync types
export interface SyncConfig {
  project_root_folder: string;
  project_doc_folder: string;
  azure_connection_string: string;
}

export interface SyncRequest {
  project_root: string;
  doc_folder: string;
  connection_string: string;
}

export interface SyncResponse {
  success: boolean;
  message: string;
  files_processed: number;
}

// UI State types
export interface EditorState {
  content: string;
  originalContent: string;
  hasUnsavedChanges: boolean;
  selectedFile: string | null;
}

export interface AppState {
  folderPath: string;
  files: FileNode[];
  selectedFile: string | null;
  editorContent: string;
  originalContent: string;
  hasUnsavedChanges: boolean;
  aiSummary: string | null;
  isLoading: boolean;
}
