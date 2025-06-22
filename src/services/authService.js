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