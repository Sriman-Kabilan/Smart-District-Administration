import React from 'react';
import { Card, Alert } from 'antd';

const Reports = () => {
  return (
    <div>
      <h1>Reports</h1>
      <Alert
        message="Reports Generation Module"
        description="Generate and download various administrative reports and analytics."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      <Card title="Report Dashboard">
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          Report generation interface will be implemented here
        </div>
      </Card>
    </div>
  );
};

export default Reports;