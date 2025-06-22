import React, { useState } from 'react';
import { Card, Row, Col, Select, Button, Table, Tag, Statistic, Alert, Tabs, Space } from 'antd';
import { MapContainer, TileLayer, Marker, Popup, Polygon } from 'react-leaflet';
import { EnvironmentOutlined, EyeOutlined, DownloadOutlined } from '@ant-design/icons';
import 'leaflet/dist/leaflet.css';

const { Option } = Select;
const { TabPane } = Tabs;

const GeospatialView = () => {
  const [selectedLayer, setSelectedLayer] = useState('infrastructure');
  const [selectedDepartment, setSelectedDepartment] = useState(null);

  const departments = ['Administration', 'Health', 'Education', 'Public Safety', 'Public Works', 'Transportation'];

  const infrastructureColumns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'type', key: 'type', render: (type) => <Tag>{type}</Tag> },
    { title: 'Department', dataIndex: 'department', key: 'department' },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (status) => <Tag color="green">{status || 'Active'}</Tag> },
    { title: 'Coordinates', key: 'coordinates', render: () => 'Connect to GIS system' }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Geospatial Analysis & Mapping</h1>
        <Space>
          <Select placeholder="Select Layer" style={{ width: 150 }} value={selectedLayer} onChange={setSelectedLayer}>
            <Option value="infrastructure">Infrastructure</Option>
            <Option value="zones">Zone Analysis</Option>
            <Option value="demographics">Demographics</Option>
            <Option value="services">Services</Option>
          </Select>
          <Select placeholder="Filter by Department" style={{ width: 200 }} allowClear value={selectedDepartment} onChange={setSelectedDepartment}>
            {departments.map(dept => <Option key={dept} value={dept}>{dept}</Option>)}
          </Select>
          <Button icon={<DownloadOutlined />}>Export Map</Button>
        </Space>
      </div>

      <Alert
        message="Geospatial Analytics Platform"
        description="Connect to your GIS systems for real-time mapping of district infrastructure, demographics, and service coverage analysis."
        type="info"
        showIcon
        style={{ marginBottom: '24px' }}
      />

      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic title="Total Infrastructure" value={0} prefix={<EnvironmentOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Operational Status" value={0} suffix="/0" />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Coverage Zones" value={0} prefix={<EyeOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Total Population" value={0} formatter={(value) => value.toLocaleString()} />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="1">
        <TabPane tab="Interactive Map" key="1">
          <Card>
            <div style={{ height: '500px', width: '100%', border: '1px solid #d9d9d9', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#fafafa' }}>
              <div style={{ textAlign: 'center', color: '#666' }}>
                <EnvironmentOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
                <div>Connect to your GIS system to display interactive maps</div>
                <div style={{ fontSize: '12px', marginTop: '8px' }}>Supports OpenStreetMap, Google Maps, and custom tile servers</div>
              </div>
            </div>
          </Card>
        </TabPane>

        <TabPane tab="Infrastructure Data" key="2">
          <Card title="Infrastructure Assets">
            <Table dataSource={[]} columns={infrastructureColumns} pagination={{ pageSize: 10 }} size="small" locale={{ emptyText: 'Connect to infrastructure database to view assets' }} />
          </Card>
        </TabPane>

        <TabPane tab="Zone Analysis" key="3">
          <Card title="Administrative Zones">
            <Table 
              dataSource={[]} 
              columns={[
                { title: 'Zone Name', dataIndex: 'name', key: 'name' },
                { title: 'Type', dataIndex: 'type', key: 'type', render: (type) => <Tag>{type}</Tag> },
                { title: 'Population', dataIndex: 'population', key: 'population' },
                { title: 'Area', key: 'area', render: () => 'Calculate from coordinates' }
              ]} 
              pagination={false} 
              size="small" 
              locale={{ emptyText: 'Connect to zoning database to view administrative zones' }}
            />
          </Card>
        </TabPane>

        <TabPane tab="Service Coverage" key="4">
          <Row gutter={16}>
            <Col span={12}>
              <Card title="Service Coverage Analysis">
                <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
                  Service coverage heatmaps will display here
                </div>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="Accessibility Metrics">
                <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
                  Accessibility analysis and metrics will display here
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Demographics" key="5">
          <Card title="Population Demographics">
            <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
              Demographic overlays and population distribution analysis will display here
            </div>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default GeospatialView;