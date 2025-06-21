import React from 'react';
import { Card, Alert } from 'antd';

const ResourceManagement = () => {
  return (
    <div>
      <h1>Resource Management</h1>
      <Alert
        message="Resource Management Module"
        description="This page will handle budget allocation, staff distribution, and equipment management."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      <Card title="Resource Allocation">
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          Resource management interface will be implemented here
        </div>
      </Card>
    </div>
  );
};

export default ResourceManagement;