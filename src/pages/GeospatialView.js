import React, { useState } from 'react';
import { 
  Card, Row, Col, Select, Button, Table, Tag, Statistic, 
  Space, Badge, Tabs, message 
} from 'antd';
import { 
  EnvironmentOutlined, EyeOutlined, AlertOutlined, 
  CheckCircleOutlined, BuildOutlined, CompassOutlined, FilterOutlined 
} from '@ant-design/icons';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const { Option } = Select;

// Custom Leaflet DivIcon generator to avoid missing image asset 404s
const createCustomIcon = (bgColor, iconText) => {
  return L.divIcon({
    className: 'custom-map-marker',
    html: `<div style="
      background-color: ${bgColor};
      width: 32px;
      height: 32px;
      border-radius: 50%;
      border: 2px solid white;
      box-shadow: 0 2px 6px rgba(0,0,0,0.35);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
      font-size: 13px;
    ">${iconText}</div>`,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16]
  });
};

const facilityIcon = createCustomIcon('#1890ff', '🏛️');
const grievanceIcon = createCustomIcon('#f5222d', '⚠️');
const workIcon = createCustomIcon('#fa8c16', '🚧');

// District Center Coordinates (Sample Metropol District)
const DISTRICT_CENTER = [28.6139, 77.2090]; // Standard coordinates (Delhi NCR / Central District)

// Spatial Datasets
const spatialPoints = [
  {
    id: 1,
    name: 'District Central Civil Hospital',
    type: 'facility',
    category: 'Healthcare Facility',
    department: 'Health & Sanitation',
    ward: 'Ward 1 - Central',
    position: [28.6250, 77.2150],
    status: 'Operational',
    details: '500-bed apex trauma & emergency facility. 12 ambulances stationed.',
    icon: facilityIcon,
    color: 'blue'
  },
  {
    id: 2,
    name: 'Main Canal Road Pothole Cluster',
    type: 'grievance',
    category: 'Road Damage / Hazard',
    department: 'Public Works',
    ward: 'Ward 2 - Riverside',
    position: [28.6050, 77.1980],
    status: 'Inspection Scheduled',
    details: 'Heavy monsoon road surface degradation across 200m stretch. Crew assigned.',
    icon: grievanceIcon,
    color: 'red'
  },
  {
    id: 3,
    name: 'Ring Road Flyover Expansion Project',
    type: 'work',
    category: 'Civil Infrastructure',
    department: 'Public Works',
    ward: 'Ward 4 - Metro Industrial',
    position: [28.6320, 77.2280],
    status: 'In Progress (72%)',
    details: 'Six-lane elevated connector bridge. Target completion: Feb 2027.',
    icon: workIcon,
    color: 'orange'
  },
  {
    id: 4,
    name: 'East Ward High-Volume Waste Transfer Station',
    type: 'facility',
    category: 'Sanitation Hub',
    department: 'Health & Sanitation',
    ward: 'Ward 3 - East Hills',
    position: [28.5980, 77.2340],
    status: 'Operational',
    details: 'Automated 120-tonne daily solid waste compaction depot.',
    icon: facilityIcon,
    color: 'blue'
  },
  {
    id: 5,
    name: 'Water Mainline Rupture at Sector 8',
    type: 'grievance',
    category: 'Water Utility Emergency',
    department: 'Public Works',
    ward: 'Ward 1 - Central',
    position: [28.6190, 77.2050],
    status: 'Repair Underway',
    details: '14-inch pressurized drinking water feeder line leak. Flow diverted.',
    icon: grievanceIcon,
    color: 'red'
  },
  {
    id: 6,
    name: 'Government Model Senior Secondary School #4',
    type: 'facility',
    category: 'Education Facility',
    department: 'Education',
    ward: 'Ward 5 - South Suburbs',
    position: [28.5910, 77.2100],
    status: 'Operational',
    details: 'Smart classrooms, 1,200 enrolled students. Clean water plant verified.',
    icon: facilityIcon,
    color: 'blue'
  }
];

const wardStatistics = [
  { key: '1', ward: 'Ward 1 - Central', population: '84,200', activeWorks: 3, openGrievances: 4, patrols: 6, status: 'Normal' },
  { key: '2', ward: 'Ward 2 - Riverside', population: '62,500', activeWorks: 2, openGrievances: 7, patrols: 4, status: 'High Alert' },
  { key: '3', ward: 'Ward 3 - East Hills', population: '51,800', activeWorks: 1, openGrievances: 2, patrols: 3, status: 'Normal' },
  { key: '4', ward: 'Ward 4 - Metro Industrial', population: '98,400', activeWorks: 5, openGrievances: 8, patrols: 8, status: 'Under Works' },
  { key: '5', ward: 'Ward 5 - South Suburbs', population: '73,100', activeWorks: 2, openGrievances: 3, patrols: 5, status: 'Normal' }
];

const GeospatialView = () => {
  const [selectedLayer, setSelectedLayer] = useState('all');
  const [selectedWard, setSelectedWard] = useState('all');

  const filteredPoints = spatialPoints.filter(p => {
    const matchesLayer = selectedLayer === 'all' || p.type === selectedLayer;
    const matchesWard = selectedWard === 'all' || p.ward === selectedWard;
    return matchesLayer && matchesWard;
  });

  const columns = [
    { title: 'Asset / Location', dataIndex: 'name', key: 'name', render: t => <strong>{t}</strong> },
    { title: 'Category', dataIndex: 'category', key: 'category' },
    { title: 'Department', dataIndex: 'department', key: 'department', render: d => <Tag color="blue">{d}</Tag> },
    { title: 'Ward', dataIndex: 'ward', key: 'ward' },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: s => {
        const color = s.includes('Operational') ? 'green' : s.includes('Repair') || s.includes('Progress') ? 'orange' : 'red';
        return <Tag color={color}>{s}</Tag>;
      }
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, r) => (
        <Button size="small" type="link" onClick={() => message.info(`Pinned to ${r.name}`)}>
          Locate
        </Button>
      )
    }
  ];

  const wardColumns = [
    { title: 'Ward / Zone', dataIndex: 'ward', key: 'ward', render: w => <strong>{w}</strong> },
    { title: 'Citizen Population', dataIndex: 'population', key: 'population' },
    { title: 'Active Infrastructure Works', dataIndex: 'activeWorks', key: 'activeWorks', render: c => <Badge count={c} style={{ backgroundColor: '#fa8c16' }} /> },
    { title: 'Unresolved Complaints', dataIndex: 'openGrievances', key: 'openGrievances', render: g => <Badge count={g} style={{ backgroundColor: '#f5222d' }} /> },
    { title: 'Patrol Teams On-duty', dataIndex: 'patrols', key: 'patrols' },
    { 
      title: 'Zone Rating', 
      dataIndex: 'status', 
      key: 'status',
      render: st => <Tag color={st === 'High Alert' ? 'red' : st === 'Under Works' ? 'orange' : 'green'}>{st}</Tag>
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>District Geospatial Intelligence & GIS Map</h1>
          <span style={{ color: '#8c8c8c' }}>Live spatial tracking of civic assets, active civil construction, and citizen grievance clusters</span>
        </div>
        <Space wrap>
          <Select value={selectedLayer} onChange={setSelectedLayer} style={{ width: 180 }}>
            <Option value="all">🗺️ All Map Layers</Option>
            <Option value="facility">🏛️ Civic Facilities</Option>
            <Option value="grievance">⚠️ Citizen Incidents</Option>
            <Option value="work">🚧 Infrastructure Works</Option>
          </Select>
          <Select value={selectedWard} onChange={setSelectedWard} style={{ width: 200 }}>
            <Option value="all">All District Wards</Option>
            <Option value="Ward 1 - Central">Ward 1 - Central</Option>
            <Option value="Ward 2 - Riverside">Ward 2 - Riverside</Option>
            <Option value="Ward 3 - East Hills">Ward 3 - East Hills</Option>
            <Option value="Ward 4 - Metro Industrial">Ward 4 - Metro Industrial</Option>
            <Option value="Ward 5 - South Suburbs">Ward 5 - South Suburbs</Option>
          </Select>
          <Button icon={<EnvironmentOutlined />} onClick={() => message.info('Recalibrating GPS base station')}>Recenter</Button>
        </Space>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f0f5ff', borderColor: '#adc6ff' }}>
            <Statistic
              title="Cataloged Civic Facilities"
              value={spatialPoints.filter(p => p.type === 'facility').length}
              suffix="hubs"
              prefix={<BuildOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1d39c4', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>Hospitals, Schools & Depots</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff1f0', borderColor: '#ffa39e' }}>
            <Statistic
              title="Geo-tagged Incidents"
              value={spatialPoints.filter(p => p.type === 'grievance').length}
              suffix="hotspots"
              prefix={<AlertOutlined style={{ color: '#f5222d' }} />}
              valueStyle={{ color: '#cf1322', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#f5222d' }}>Potholes & Water Leakages</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff7e6', borderColor: '#ffd591' }}>
            <Statistic
              title="Civil Construction Zones"
              value={spatialPoints.filter(p => p.type === 'work').length}
              suffix="projects"
              prefix={<CompassOutlined style={{ color: '#fa8c16' }} />}
              valueStyle={{ color: '#d46b08', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#fa8c16' }}>Active road & flyover sites</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed', borderColor: '#b7eb8f' }}>
            <Statistic
              title="District Geographic Coverage"
              value={100}
              suffix="%"
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#389e0d', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>All 5 Wards Telemetry Connected</div>
          </Card>
        </Col>
      </Row>

      {/* Interactive Leaflet Map */}
      <Card 
        title="Interactive District GIS Map" 
        style={{ marginBottom: '24px' }}
        extra={
          <Space>
            <span><span style={{ color: '#1890ff', fontSize: 16 }}>●</span> Facilities</span>
            <span><span style={{ color: '#f5222d', fontSize: 16 }}>●</span> Grievances</span>
            <span><span style={{ color: '#fa8c16', fontSize: 16 }}>●</span> Active Works</span>
          </Space>
        }
      >
        <div style={{ height: '480px', width: '100%', borderRadius: '8px', overflow: 'hidden' }}>
          <MapContainer 
            center={DISTRICT_CENTER} 
            zoom={13} 
            scrollWheelZoom={false}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {filteredPoints.map((point) => (
              <Marker key={point.id} position={point.position} icon={point.icon}>
                <Popup>
                  <div style={{ minWidth: 200 }}>
                    <h4 style={{ margin: '0 0 6px 0', color: '#1890ff' }}>{point.name}</h4>
                    <div><strong>Category:</strong> {point.category}</div>
                    <div><strong>Department:</strong> {point.department}</div>
                    <div><strong>Ward:</strong> {point.ward}</div>
                    <div style={{ marginTop: 4 }}>
                      <Tag color={point.color}>{point.status}</Tag>
                    </div>
                    <p style={{ margin: '6px 0 0 0', fontSize: 12, color: '#595959' }}>{point.details}</p>
                  </div>
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      </Card>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={14}>
          <Card title="Ward Demographics & Incident Density">
            <Table dataSource={wardStatistics} columns={wardColumns} pagination={false} size="middle" />
          </Card>
        </Col>
        <Col xs={24} lg={10}>
          <Card title="Spatial Asset Registry">
            <Table dataSource={filteredPoints} columns={columns} pagination={{ pageSize: 4 }} size="small" />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default GeospatialView;
