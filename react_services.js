// services/api.js - Base API Configuration
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

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

export default api;

// services/auth.js - Authentication Service
import api from './api';

export const authService = {
  async login(username, password) {
    const response = await api.post('/auth/login', {
      username,
      password,
    });
    return response.data;
  },

  async register(userData) {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me');
    return response.data;
  },

  async getAllUsers() {
    const response = await api.get('/auth/users');
    return response.data;
  },

  async updateUser(userId, userData) {
    const response = await api.put(`/auth/users/${userId}`, userData);
    return response.data;
  },

  async deleteUser(userId) {
    const response = await api.delete(`/auth/users/${userId}`);
    return response.data;
  },
};

// services/dashboard.js - Dashboard Data Service
import api from './api';

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

// services/tasks.js - Task Management Service
import api from './api';

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

  async addTaskComment(taskId, comment) {
    const response = await api.post(`/tasks/${taskId}/comments`, { text: comment });
    return response.data;
  },

  async getTaskComments(taskId) {
    const response = await api.get(`/tasks/${taskId}/comments`);
    return response.data;
  },

  async deleteTask(taskId) {
    const response = await api.delete(`/tasks/${taskId}`);
    return response.data;
  },
};

// services/analytics.js - Predictive Analytics Service
import api from './api';

export const analyticsService = {
  async getPredictions(department, periods = 3, modelType = 'random_forest') {
    const response = await api.get('/analytics/predictions', {
      params: { department, periods, model_type: modelType }
    });
    return response.data;
  },

  async getOptimalAllocation(department) {
    const response = await api.get(`/analytics/optimization/${department}`);
    return response.data;
  },

  async runScenarioAnalysis(department, scenarios) {
    const response = await api.post('/analytics/scenarios', {
      department,
      scenarios
    });
    return response.data;
  },

  async getResourceTrends(department, timeRange = '12m') {
    const response = await api.get('/analytics/trends', {
      params: { department, time_range: timeRange }
    });
    return response.data;
  },

  async generateInsights(department) {
    const response = await api.get(`/analytics/insights/${department}`);
    return response.data;
  },
};

// hooks/useAuth.js - Authentication Hook
import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// hooks/useApi.js - Generic API Hook
import { useState, useEffect } from 'react';

export const useApi = (apiFunction, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await apiFunction();
        setData(result);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, dependencies);

  const refetch = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await apiFunction();
      setData(result);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, refetch };
};

// utils/constants.js - Application Constants
export const USER_ROLES = {
  ADMINISTRATOR: 'administrator',
  DEPARTMENT_HEAD: 'department_head',
  STAFF: 'staff',
};

export const TASK_STATUSES = {
  PENDING: 'Pending',
  IN_PROGRESS: 'In Progress',
  COMPLETED: 'Completed',
  CANCELED: 'Canceled',
};

export const TASK_PRIORITIES = {
  LOW: 'Low',
  MEDIUM: 'Medium',
  HIGH: 'High',
  CRITICAL: 'Critical',
};

export const DEPARTMENTS = [
  'Public Works',
  'Education',
  'Health',
  'Finance',
  'Urban Planning',
  'Transportation',
  'Social Services',
];

export const CHART_COLORS = {
  PRIMARY: '#1890ff',
  SUCCESS: '#52c41a',
  WARNING: '#faad14',
  ERROR: '#f5222d',
  INFO: '#13c2c2',
};

// utils/helpers.js - Utility Functions
import moment from 'moment';

export const formatCurrency = (amount, currency = 'USD') => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
};

export const formatNumber = (number, options = {}) => {
  return new Intl.NumberFormat('en-US', options).format(number);
};

export const formatDate = (date, format = 'MMM DD, YYYY') => {
  return moment(date).format(format);
};

export const getTimeAgo = (date) => {
  return moment(date).fromNow();
};

export const calculatePercentageChange = (current, previous) => {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
};

export const getStatusColor = (status) => {
  const colors = {
    'Pending': 'orange',
    'In Progress': 'blue',
    'Completed': 'green',
    'Canceled': 'red',
  };
  return colors[status] || 'default';
};

export const getPriorityColor = (priority) => {
  const colors = {
    'Low': 'green',
    'Medium': 'orange',
    'High': 'red',
    'Critical': 'purple',
  };
  return colors[priority] || 'default';
};

export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

export const generateTaskId = () => {
  return `T-${Date.now().toString().slice(-6)}`;
};