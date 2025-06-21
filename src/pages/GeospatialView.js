import React from 'react';
import { Card, Alert } from 'antd';

const GeospatialView = () => {
  return (
    <div>
      <h1>Geospatial View</h1>
      <Alert
        message="Geospatial Visualization Module"
        description="Interactive maps showing district data, service locations, and geographical analytics."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      <Card title="District Map">
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          Interactive geospatial maps will be implemented here
        </div>
      </Card>
    </div>
  );
};

export default GeospatialView;