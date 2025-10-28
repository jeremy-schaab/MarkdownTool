import axios from 'axios';
import type {
  FileNode,
  FileContent,
  SaveFileRequest,
  CreateFileRequest,
  AISummaryTemplate,
  AISummaryRequest,
  AISummaryResponse,
  SyncConfig,
  SyncRequest,
  SyncResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// File Operations
export const fileAPI = {
  list: async (folderPath: string): Promise<FileNode[]> => {
    const response = await api.get('/api/files/list', {
      params: { folder_path: folderPath },
    });
    return response.data;
  },

  read: async (filePath: string): Promise<FileContent> => {
    const response = await api.get('/api/files/content', {
      params: { file_path: filePath },
    });
    return response.data;
  },

  save: async (request: SaveFileRequest): Promise<{ success: boolean; message: string }> => {
    const response = await api.post('/api/files/save', request);
    return response.data;
  },

  create: async (request: CreateFileRequest): Promise<{ success: boolean; path: string }> => {
    const response = await api.post('/api/files/create', request);
    return response.data;
  },

  delete: async (filePath: string): Promise<{ success: boolean; message: string }> => {
    const response = await api.delete('/api/files/delete', {
      params: { file_path: filePath },
    });
    return response.data;
  },

  upload: async (file: File, folderPath: string): Promise<{ success: boolean; path: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('folder_path', folderPath);

    const response = await api.post('/api/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  download: async (filePath: string): Promise<Blob> => {
    const response = await api.get('/api/files/download', {
      params: { file_path: filePath },
      responseType: 'blob',
    });
    return response.data;
  },

  search: async (folderPath: string, query: string): Promise<FileNode[]> => {
    const response = await api.get('/api/files/search', {
      params: { folder_path: folderPath, query },
    });
    return response.data;
  },
};

// AI Operations
export const aiAPI = {
  getTemplates: async (): Promise<AISummaryTemplate[]> => {
    const response = await api.get('/api/ai/templates');
    return response.data;
  },

  summarize: async (request: AISummaryRequest): Promise<AISummaryResponse> => {
    const response = await api.post('/api/ai/summarize', request);
    return response.data;
  },

  saveSummary: async (
    summary: string,
    originalFilePath: string,
    templateName: string
  ): Promise<{ success: boolean; path: string }> => {
    const response = await api.post('/api/ai/save-summary', {
      summary,
      original_file_path: originalFilePath,
      template_name: templateName,
    });
    return response.data;
  },

  estimateTokens: async (content: string): Promise<{ estimated_tokens: number }> => {
    const response = await api.get('/api/ai/estimate-tokens', {
      params: { content },
    });
    return response.data;
  },
};

// Sync Operations
export const syncAPI = {
  push: async (request: SyncRequest): Promise<SyncResponse> => {
    const response = await api.post('/api/sync/push', request);
    return response.data;
  },

  pull: async (request: SyncRequest): Promise<SyncResponse> => {
    const response = await api.post('/api/sync/pull', request);
    return response.data;
  },

  saveConfig: async (config: SyncConfig): Promise<{ success: boolean; message: string }> => {
    const response = await api.post('/api/sync/save-config', config);
    return response.data;
  },

  loadConfig: async (projectRoot: string): Promise<SyncConfig> => {
    const response = await api.post('/api/sync/load-config', {
      project_root: projectRoot,
    });
    return response.data;
  },
};

export default api;
