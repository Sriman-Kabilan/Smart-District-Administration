import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    console.log('AuthContext: Checking token', token ? 'exists' : 'not found');
    
    if (token) {
      authService.getCurrentUser()
        .then((userData) => {
          console.log('AuthContext: User data received', userData);
          setUser(userData);
        })
        .catch((error) => {
          console.log('AuthContext: Failed to get user', error);
          localStorage.removeItem('token');
        })
        .finally(() => {
          console.log('AuthContext: Loading complete');
          setLoading(false);
        });
    } else {
      console.log('AuthContext: No token, setting loading to false');
      setLoading(false);
    }
  }, []);

  const login = async (username, password) => {
    const response = await authService.login(username, password);
    localStorage.setItem('token', response.access_token);
    setUser(response.user);
    return response;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
