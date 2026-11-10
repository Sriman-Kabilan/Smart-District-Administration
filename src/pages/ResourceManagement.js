import React, { useState } from 'react';
import { 
  Card, Row, Col, Table, Button, Modal, Form, Input, Select, InputNumber, 
  Tabs, Progress, Statistic, Tag, Space, message, Badge 
} from 'antd';
import { 
  PlusOutlined, ToolOutlined, DollarOutlined, 
  CheckCircleOutlined, SyncOutlined, CarOutlined, BankOutlined, TeamOutlined 
} from '@ant-design/icons';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell 
} from 'recharts';

const { Option } = Select;

// Budget Dataset
const initialBudgets = [
  { key: '1', department: 'Public Works', allocated: 4500000, spent: 3420000, remaining: 1080000, utilization: 76.0 },
  { key: '2', department: 'Health & Sanitation', allocated: 3200000, spent: 2480000, remaining: 720000, utilization: 77.5 },
  { key: '3', department: 'Transportation', allocated: 2100000, spent: 1575000, remaining: 525000, utilization: 75.0 },
  { key: '4', department: 'Education', allocated: 1500000, spent: 1050000, remaining: 450000, utilization: 70.0 },
  { key: '5', department: 'Revenue & Finance', allocated: 850000, spent: 510000, remaining: 340000, utilization: 60.0 },
  { key: '6', department: 'IT & Digital Services', allocated: 950000, spent: 684000, remaining: 266000, utilization: 72.0 }
];

// Equipment Dataset
const initialEquipment = [
  { key: '1', assetId: 'EQ-PW-101', name: 'CAT Hydraulic Excavator', department: 'Public Works', status: 'Active', condition: 'Optimal', location: 'Zone 3 Ward 12', nextMaintenance: '2026-12-15' },
  { key: '2', assetId: 'EQ-HS-204', name: 'Advanced Life Support Ambulance', department: 'Health & Sanitation', status: 'Active', condition: 'Optimal', location: 'District General Hospital', nextMaintenance: '2026-11-28' },
  { key: '3', assetId: 'EQ-TR-308', name: 'Electric Low-Floor City Bus', department: 'Transportation', status: 'Under Maintenance', condition: 'Fair', location: 'Depot #2 Workshop', nextMaintenance: '2026-11-12' },
  { key: '4', assetId: 'EQ-PW-109', name: 'Vibratory Asphalt Road Roller', department: 'Public Works', status: 'Active', condition: 'Optimal', location: 'North Arterial Flyover', nextMaintenance: '2026-12-01' },
  { key: '5', assetId: 'EQ-HS-215', name: 'High-Capacity Waste Compactor', department: 'Health & Sanitation', status: 'Active', condition: 'Optimal', location: 'Sector 7 Transfer Station', nextMaintenance: '2026-11-20' },
  { key: '6', assetId: 'EQ-IT-402', name: 'Mobile Command Communications Van', department: 'IT & Digital Services', status: 'Standby', condition: 'Optimal', location: 'District HQ Emergency Bay', nextMaintenance: '2027-01-10' }
];

// Staff Distribution
const staffDistribution = [
  { department: 'Public Works', staff: 142, fieldCrew: 110, office: 32, fill: '#1890ff' },
  { department: 'Health & Sanitation', staff: 185, fieldCrew: 140, office: 45, fill: '#52c41a' },
  { department: 'Transportation', staff: 98, fieldCrew: 75, office: 23, fill: '#faad14' },
  { department: 'Education', staff: 65, fieldCrew: 15, office: 50, fill: '#722ed1' },
  { department: 'Revenue & Finance', staff: 42, fieldCrew: 8, office: 34, fill: '#13c2c2' },
  { department: 'IT & Digital Services', staff: 38, fieldCrew: 12, office: 26, fill: '#eb2f96' }
];

const ResourceManagement = () => {
  const [budgets, setBudgets] = useState(initialBudgets);
  const [equipmentList, setEquipmentList] = useState(initialEquipment);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('1');
  const [form] = Form.useForm();

  // Calculations
  const totalAllocated = budgets.reduce((acc, curr) => acc + curr.allocated, 0);
  const totalSpent = budgets.reduce((acc, curr) => acc + curr.spent, 0);
  const totalRemaining = totalAllocated - totalSpent;
  const overallBurnRate = ((totalSpent / totalAllocated) * 100).toFixed(1);

  const handleAddEquipment = (values) => {
    const newEntry = {
      key: `${Date.now()}`,
      assetId: `EQ-${values.department.substring(0, 2).toUpperCase()}-${Math.floor(100 + Math.random() * 900)}`,
      name: values.name,
      department: values.department,
      status: values.status || 'Active',
      condition: 'Optimal',
      location: values.location || 'Central Depot',
      nextMaintenance: values.nextMaintenance || '2027-01-01'
    };
    setEquipmentList([newEntry, ...equipmentList]);
    message.success(`Resource ${newEntry.assetId} successfully cataloged.`);
    setIsModalOpen(false);
    form.resetFields();
  };

  const budgetColumns = [
    { title: 'Department', dataIndex: 'department', key: 'department', render: text => <strong>{text}</strong> },
    { title: 'Allocated Budget', dataIndex: 'allocated', key: 'allocated', render: v => `$${v.toLocaleString()}` },
    { title: 'Expenditure to Date', dataIndex: 'spent', key: 'spent', render: v => <span style={{ color: '#cf1322' }}>${v.toLocaleString()}</span> },
    { title: 'Available Funds', dataIndex: 'remaining', key: 'remaining', render: v => <span style={{ color: '#389e0d' }}>${v.toLocaleString()}</span> },
    { 
      title: 'Budget Burn %', 
      key: 'utilization', 
      render: (_, r) => (
        <Progress 
          percent={r.utilization} 
          status={r.utilization > 85 ? 'exception' : 'active'}
          strokeColor={r.utilization > 80 ? '#f5222d' : '#1890ff'}
          size="small" 
        />
      ) 
    }
  ];

  const equipmentColumns = [
    { title: 'Asset Tag', dataIndex: 'assetId', key: 'assetId', render: tag => <Tag color="geekblue">{tag}</Tag> },
    { title: 'Equipment Name', dataIndex: 'name', key: 'name', render: t => <strong>{t}</strong> },
    { title: 'Assigned Department', dataIndex: 'department', key: 'department' },
    { 
      title: 'Operational Status', 
      dataIndex: 'status', 
      key: 'status',
      render: s => {
        const color = s === 'Active' ? 'green' : s === 'Under Maintenance' ? 'orange' : 'default';
        return <Tag color={color}>{s}</Tag>;
      }
    },
    { title: 'Deployment Location', dataIndex: 'location', key: 'location' },
    { title: 'Next Service Due', dataIndex: 'nextMaintenance', key: 'nextMaintenance' },
    {
      title: 'Action',
      key: 'action',
      render: (_, r) => (
        <Button 
          size="small" 
          icon={<ToolOutlined />}
          onClick={() => message.info(`Dispatched service inquiry for ${r.assetId}`)}
        >
          Inspect
        </Button>
      )
    }
  ];

  const staffColumns = [
    { title: 'Department', dataIndex: 'department', key: 'department', render: t => <strong>{t}</strong> },
    { title: 'Total Workforce', dataIndex: 'staff', key: 'staff', render: s => <Badge count={s} overflowCount={999} style={{ backgroundColor: '#108ee9' }} /> },
    { title: 'Field Crew Deployments', dataIndex: 'fieldCrew', key: 'fieldCrew' },
    { title: 'Administrative & Ops', dataIndex: 'office', key: 'office' },
    { 
      title: 'Field Ratio', 
      key: 'ratio', 
      render: (_, r) => `${Math.round((r.fieldCrew / r.staff) * 100)}% on-ground` 
    }
  ];

  const tabItems = [
    {
      key: '1',
      label: 'Budget & Expenditure',
      children: (
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={15}>
            <Card title="Departmental Budget vs Current Expenditure">
              <div style={{ height: 320 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={budgets}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="department" tick={{ fontSize: 11 }} />
                    <YAxis tickFormatter={v => `$${(v/1000000).toFixed(1)}M`} />
                    <Tooltip formatter={v => `$${Number(v).toLocaleString()}`} />
                    <Legend />
                    <Bar dataKey="allocated" name="Allocated Budget" fill="#d9d9d9" />
                    <Bar dataKey="spent" name="Expended" fill="#1890ff" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </Col>
          <Col xs={24} lg={9}>
            <Card title="Departmental Share of Expenditure">
              <div style={{ height: 320 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={budgets} dataKey="spent" nameKey="department" cx="50%" cy="50%" outerRadius={90} label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                      {staffDistribution.map((entry, idx) => (
                        <Cell key={`cell-${idx}`} fill={entry.fill} />
                      ))}
                    </Pie>
                    <Tooltip formatter={v => `$${Number(v).toLocaleString()}`} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </Col>
          <Col span={24}>
            <Card title="Financial Ledger & Utilization Breakdown">
              <Table dataSource={budgets} columns={budgetColumns} pagination={false} size="middle" />
            </Card>
          </Col>
        </Row>
      )
    },
    {
      key: '2',
      label: 'Heavy Machinery & Fleet Assets',
      children: (
        <Card 
          title="District Heavy Equipment & Fleet Registry"
          extra={<Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>Add Fleet Asset</Button>}
        >
          <Table dataSource={equipmentList} columns={equipmentColumns} pagination={{ pageSize: 5 }} size="middle" />
        </Card>
      )
    },
    {
      key: '3',
      label: 'Human Resources & Field Deployment',
      children: (
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={14}>
            <Card title="Staff Distribution & Deployment Readiness">
              <Table dataSource={staffDistribution} columns={staffColumns} pagination={false} size="middle" />
            </Card>
          </Col>
          <Col xs={24} lg={10}>
            <Card title="District Personnel Allocation">
              <div style={{ height: 300 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={staffDistribution} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" horizontal={false} />
                    <XAxis type="number" />
                    <YAxis dataKey="department" type="category" width={120} tick={{ fontSize: 11 }} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="fieldCrew" name="Field Deployments" fill="#52c41a" stackId="a" />
                    <Bar dataKey="office" name="HQ / Administrative" fill="#1890ff" stackId="a" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </Col>
        </Row>
      )
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>District Resource Management</h1>
          <span style={{ color: '#8c8c8c' }}>Financial appropriations, equipment logistics, and workforce deployment control</span>
        </div>
        <Space>
          <Button icon={<SyncOutlined />} onClick={() => message.success('Telemetry re-synced with treasury ledger')}>Sync Treasury</Button>
          <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>Register Resource</Button>
        </Space>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f0f5ff', borderColor: '#adc6ff' }}>
            <Statistic
              title="Total District Budget"
              value={totalAllocated}
              formatter={v => `$${Number(v).toLocaleString()}`}
              prefix={<BankOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1d39c4', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>Fiscal Year 2026/27 Approved</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff7e6', borderColor: '#ffd591' }}>
            <Statistic
              title="Expenditure Burn Rate"
              value={overallBurnRate}
              precision={1}
              suffix="%"
              prefix={<DollarOutlined style={{ color: '#fa8c16' }} />}
              valueStyle={{ color: '#d46b08', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#fa8c16' }}>${totalSpent.toLocaleString()} disbursed</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed', borderColor: '#b7eb8f' }}>
            <Statistic
              title="Available Contingency"
              value={totalRemaining}
              formatter={v => `$${Number(v).toLocaleString()}`}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#389e0d', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>Uncommitted fiscal balance</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f9f0ff', borderColor: '#d3adf7' }}>
            <Statistic
              title="Active Fleet & Equipment"
              value={equipmentList.length}
              suffix={`/ ${equipmentList.length + 3} units`}
              prefix={<CarOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#531dab', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#722ed1' }}>94% operational readiness</div>
          </Card>
        </Col>
      </Row>

      <Tabs activeKey={activeTab} onChange={setActiveTab} items={tabItems} />

      <Modal
        title="Register New Municipal Asset / Equipment"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleAddEquipment}>
          <Form.Item name="name" label="Asset / Equipment Name" rules={[{ required: true, message: 'Please input asset name' }]}>
            <Input placeholder="e.g. Caterpillar Backhoe Loader" />
          </Form.Item>
          <Form.Item name="department" label="Assigned Department" rules={[{ required: true, message: 'Select department' }]}>
            <Select placeholder="Select department">
              {budgets.map(b => <Option key={b.department} value={b.department}>{b.department}</Option>)}
            </Select>
          </Form.Item>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="status" label="Initial Status" initialValue="Active">
                <Select>
                  <Option value="Active">Active</Option>
                  <Option value="Standby">Standby</Option>
                  <Option value="Under Maintenance">Under Maintenance</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="location" label="Station / Ward Location" initialValue="Central Depot">
                <Input placeholder="e.g. Ward 4 Depot" />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item name="nextMaintenance" label="Scheduled Service Date" initialValue="2026-12-30">
            <Input type="date" />
          </Form.Item>
          <div style={{ textAlign: 'right', marginTop: 16 }}>
            <Space>
              <Button onClick={() => setIsModalOpen(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit">Register Asset</Button>
            </Space>
          </div>
        </Form>
      </Modal>
    </div>
  );
};

export default ResourceManagement;
