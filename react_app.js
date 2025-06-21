// App.js - Main React Application Component
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import PerformanceMetrics from './pages/PerformanceMetrics';
import ResourceManagement from './pages/ResourceManagement';
import TaskTracking from './pages/TaskTracking';
import DepartmentCoordination from './pages/DepartmentCoordination';
import GeospatialView from './pages/GeospatialView';
import Reports from './pages/Reports';
import PredictiveAnalytics from './pages/PredictiveAnalytics';
import ProtectedRoute from './components/Auth/ProtectedRoute';
import './App.css';

const App = () => {
  return (
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
                        <Route path="/performance" element={<PerformanceMetrics />} />
                        <Route path="/resources" element={<ResourceManagement />} />
                        <Route path="/tasks" element={<TaskTracking />} />
                        <Route path="/coordination" element={<DepartmentCoordination />} />
                        <Route path="/geospatial" element={<GeospatialView />} />
                        <Route path="/reports" element={<Reports />} />
                        <Route path="/analytics" element={<PredictiveAnalytics />} />
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
  );
};

export default App;