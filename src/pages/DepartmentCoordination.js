import React from 'react';
import { Card, Alert } from 'antd';

const DepartmentCoordination = () => {
  return (
    <div>
      <h1>Department Coordination</h1>
      <Alert
        message="Department Coordination Module"
        description="Inter-departmental collaboration and communication tools."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      <Card title="Coordination Dashboard">
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          Department coordination interface will be implemented here
        </div>
      </Card>
    </div>
  );
};

export default DepartmentCoordination;