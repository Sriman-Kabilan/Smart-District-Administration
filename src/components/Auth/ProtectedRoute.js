import React from 'react';
import { Navigate } from 'react-router-dom';
import { Spin } from 'antd';
import { useAuth } from '../../contexts/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  console.log('ProtectedRoute - User:', user, 'Loading:', loading);

  if (loading) {
    console.log('ProtectedRoute - Showing loading spinner');
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        background: '#fff'
      }}>
        <div style={{ textAlign: 'center' }}>
          <Spin size="large" />
          <p style={{ marginTop: 16, color: '#666' }}>Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    console.log('ProtectedRoute - No user, redirecting to login');
    return <Navigate to="/login" replace />;
  }

  console.log('ProtectedRoute - User authenticated, rendering children');
  return children;
};

export default ProtectedRoute;