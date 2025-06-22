import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { AuthProvider } from './contexts/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import TaskTracking from './pages/TaskTracking';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import Layout from './components/Layout/Layout';
import ErrorBoundary from './components/Common/ErrorBoundary';
import './App.css';

const App = () => {
  console.log('App component rendering');
  
  return (
    <ErrorBoundary>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: '#1890ff',
            borderRadius: 6,
          },
        }}
      >
        <AuthProvider>
          <Router>
            <div className="App">
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route
                  path="/*"
                  element={
                    <ProtectedRoute>
                      <Layout>
                        <Routes>
                          <Route path="/" element={<Navigate to="/dashboard" replace />} />
                          <Route path="/dashboard" element={<Dashboard />} />
                          <Route path="/tasks" element={<TaskTracking />} />
                          <Route path="/performance" element={<div style={{padding: '20px'}}><h1>Performance Metrics</h1><p>Performance analytics will be implemented here</p></div>} />
                          <Route path="/resources" element={<div style={{padding: '20px'}}><h1>Resource Management</h1><p>Resource allocation tools will be implemented here</p></div>} />
                          <Route path="/coordination" element={<div style={{padding: '20px'}}><h1>Department Coordination</h1><p>Inter-department collaboration tools will be implemented here</p></div>} />
                          <Route path="/geospatial" element={<div style={{padding: '20px'}}><h1>Geospatial View</h1><p>Interactive maps will be implemented here</p></div>} />
                          <Route path="/reports" element={<div style={{padding: '20px'}}><h1>Reports</h1><p>Report generation will be implemented here</p></div>} />
                          <Route path="/analytics" element={<div style={{padding: '20px'}}><h1>AI Analytics</h1><p>Predictive analytics will be implemented here</p></div>} />
                        </Routes>
                      </Layout>
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </div>
          </Router>
        </AuthProvider>
      </ConfigProvider>
    </ErrorBoundary>
  );
};

export default App;