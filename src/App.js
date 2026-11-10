import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { AuthProvider } from './contexts/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import TaskTracking from './pages/TaskTracking';
import PerformanceMetrics from './pages/PerformanceMetrics';
import ResourceManagement from './pages/ResourceManagement';
import DepartmentCoordination from './pages/DepartmentCoordination';
import GeospatialView from './pages/GeospatialView';
import Reports from './pages/Reports';
import PredictiveAnalytics from './pages/PredictiveAnalytics';
import Profile from './pages/Profile';
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
                          <Route path="/performance" element={<PerformanceMetrics />} />
                          <Route path="/resources" element={<ResourceManagement />} />
                          <Route path="/coordination" element={<DepartmentCoordination />} />
                          <Route path="/geospatial" element={<GeospatialView />} />
                          <Route path="/reports" element={<Reports />} />
                          <Route path="/analytics" element={<PredictiveAnalytics />} />
                          <Route path="/profile" element={<Profile />} />
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