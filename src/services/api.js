import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || (
  process.env.NODE_ENV === 'development' && window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'
    : '/api'
);

console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const dashboardService = {
  async getOverviewData(department = null) {
    const params = department ? { department } : {};
    const response = await api.get('/dashboard/overview', { params });
    return response.data;
  },

  async getPerformanceMetrics(department = null, dateRange = null) {
    const params = { department, ...dateRange };
    const response = await api.get('/dashboard/performance', { params });
    return response.data;
  },

  async getResourceAllocation(department = null) {
    const params = department ? { department } : {};
    const response = await api.get('/dashboard/resources', { params });
    return response.data;
  },

  async getDepartmentData(department) {
    const response = await api.get(`/dashboard/departments/${department}`);
    return response.data;
  },

  async getActivityLogs(limit = 15) {
    const response = await api.get('/dashboard/activity', { params: { limit } });
    return response.data;
  },
};

export const taskService = {
  async getTasks(filters = {}) {
    const response = await api.get('/tasks', { params: filters });
    return response.data;
  },

  async getTaskById(taskId) {
    const response = await api.get(`/tasks/${taskId}`);
    return response.data;
  },

  async createTask(taskData) {
    const response = await api.post('/tasks', taskData);
    return response.data;
  },

  async updateTask(taskId, taskData) {
    const response = await api.put(`/tasks/${taskId}`, taskData);
    return response.data;
  },

  async updateTaskStatus(taskId, status) {
    const response = await api.patch(`/tasks/${taskId}/status`, { status });
    return response.data;
  },

  async deleteTask(taskId) {
    const response = await api.delete(`/tasks/${taskId}`);
    return response.data;
  },
};

export const analyticsService = {
  async getPredictions(department, periods = 3, modelType = 'random_forest') {
    const response = await api.get('/analytics/predictions', {
      params: { department, periods, model_type: modelType }
    });
    return response.data;
  },

  async getResourceTrends(department, timeRange = '12m') {
    const response = await api.get('/analytics/trends', {
      params: { department, time_range: timeRange }
    });
    return response.data;
  },
};

export default api;