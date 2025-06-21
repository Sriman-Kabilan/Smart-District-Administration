import React from 'react';
import { Card, Alert } from 'antd';

const PerformanceMetrics = () => {
  return (
    <div>
      <h1>Performance Metrics</h1>
      <Alert
        message="Performance Metrics Module"
        description="This page will display comprehensive performance analytics and KPI dashboards."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      <Card title="Performance Overview">
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          Performance metrics and charts will be implemented here
        </div>
      </Card>
    </div>
  );
};

export default PerformanceMetrics;