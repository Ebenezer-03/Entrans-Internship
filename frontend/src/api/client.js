import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  uploadDataset: () => client.post('/upload-dataset'),
  classify: (text) => client.post('/classify', { text }),
  ragSearch: (query) => client.post('/rag-search', { query }),
  summarize: (text) => client.post('/summarize', { text }),
  benchmark: (runFull = false) => client.post('/benchmark', { run_full: runFull }),
  generatePdfReport: () => client.post('/pdf-report', {}, { responseType: 'blob' }),
  getSettings: () => client.get('/settings'),
  saveSettings: (data) => client.post('/settings', data),
  getMetrics: () => client.post('/metrics'),
  getRecentActivity: () => client.post('/recent-activity'),
};

export default api;
