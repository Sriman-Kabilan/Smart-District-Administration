import React, { useState } from 'react';
import { Card, Row, Col, Statistic, Select, DatePicker, Table, Progress, Tabs, Tag, Space, Button, message, Tooltip as AntTooltip } from 'antd';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell 
} from 'recharts';
import { 
  RiseOutlined, FallOutlined, DashboardOutlined, 
  CheckCircleOutlined, ClockCircleOutlined, AlertOutlined, ReloadOutlined 
} from '@ant-design/icons';

const { Option } = Select;
const { RangePicker } = DatePicker;

// District Performance Datasets
const monthlyTrends = [
  { month: 'Jan', slaRate: 88.5, resolved: 280, target: 300, satisfaction: 4.2 },
  { month: 'Feb', slaRate: 90.2, resolved: 310, target: 320, satisfaction: 4.3 },
  { month: 'Mar', slaRate: 91.8, resolved: 345, target: 350, satisfaction: 4.4 },
  { month: 'Apr', slaRate: 89.4, resolved: 295, target: 310, satisfaction: 4.3 },
  { month: 'May', slaRate: 93.6, resolved: 380, target: 370, satisfaction: 4.5 },
  { month: 'Jun', slaRate: 94.8, resolved: 412, target: 400, satisfaction: 4.7 }
];

const departmentComparison = [
  { department: 'Public Works', target: 450, actual: 432, slaCompliance: 92, efficiency: 88 },
  { department: 'Health & Sanitation', target: 380, actual: 395, slaCompliance: 97, efficiency: 94 },
  { department: 'Education', target: 210, actual: 205, slaCompliance: 95, efficiency: 91 },
  { department: 'Revenue & Finance', target: 320, actual: 310, slaCompliance: 93, efficiency: 89 },
  { department: 'Transportation', target: 290, actual: 265, slaCompliance: 86, efficiency: 82 },
  { department: 'Environment', target: 180, actual: 192, slaCompliance: 96, efficiency: 95 },
  { department: 'IT & Digital Services', target: 260, actual: 255, slaCompliance: 98, efficiency: 96 }
];

const departmentWorkloadPie = [
  { name: 'Public Works', value: 28, color: '#1890ff' },
  { name: 'Health & Sanitation', value: 24, color: '#52c41a' },
  { name: 'Transportation', value: 16, color: '#faad14' },
  { name: 'Revenue', value: 14, color: '#722ed1' },
  { name: 'Education', value: 10, color: '#13c2c2' },
  { name: 'Environment', value: 8, color: '#eb2f96' }
];

const kpiIndicatorsData = [
  { key: '1', indicator: 'Pothole & Road Repair Turnaround', department: 'Public Works', value: '42 hrs', target: '< 48 hrs', progress: 87, status: 'On Track' },
  { key: '2', indicator: 'Drinking Water Quality Testing', department: 'Health & Sanitation', value: '99.4%', target: '99.0%', progress: 100, status: 'Exceeded' },
  { key: '3', indicator: 'Emergency Ambulance Response', department: 'Health & Sanitation', value: '11.4 mins', target: '< 15 mins', progress: 95, status: 'On Track' },
  { key: '4', indicator: 'Property Tax Collection Drive', department: 'Revenue & Finance', value: '82.6%', target: '80.0%', progress: 100, status: 'Exceeded' },
  { key: '5', indicator: 'Public Bus Schedule Punctuality', department: 'Transportation', value: '78.2%', target: '85.0%', progress: 74, status: 'Needs Attention' },
  { key: '6', indicator: 'Streetlight Outage Restoration', department: 'Public Works', value: '18 hrs', target: '< 24 hrs', progress: 92, status: 'On Track' },
  { key: '7', indicator: 'Citizen Digital Portal Uptime', department: 'IT & Digital Services', value: '99.94%', target: '99.9%', progress: 100, status: 'Exceeded' }
];

const bottleneckData = [
  { key: '1', issue: 'Main Stormwater Culvert Clogging', department: 'Public Works', urgency: 'Critical', aging: '4 days', slaLimit: '48 hrs', owner: 'Robert Martinez', location: 'Ward 4 - River Road' },
  { key: '2', issue: 'Traffic Signal Controller Failure', department: 'Transportation', urgency: 'High', aging: '32 hrs', slaLimit: '24 hrs', owner: 'Ananya Sharma', location: 'Central Junction 5' },
  { key: '3', issue: 'Vaccine Cold Storage Maintenance', department: 'Health & Sanitation', urgency: 'High', aging: '18 hrs', slaLimit: '24 hrs', owner: 'Dr. Sarah Jenkins', location: 'District Hospital East' },
  { key: '4', issue: 'Building Permit Approval Backlog', department: 'Urban Planning', urgency: 'Medium', aging: '7 days', slaLimit: '10 days', owner: 'David Chen', location: 'Municipal Civic Center' }
];

const PerformanceMetrics = () => {
  const [selectedDept, setSelectedDept] = useState('All');
  const [activeTab, setActiveTab] = useState('1');

  const filteredComparison = selectedDept === 'All' 
    ? departmentComparison 
    : departmentComparison.filter(d => d.department === selectedDept);

  const filteredKpi = selectedDept === 'All'
    ? kpiIndicatorsData
    : kpiIndicatorsData.filter(d => d.department === selectedDept);

  const kpiColumns = [
    { title: 'Performance Indicator', dataIndex: 'indicator', key: 'indicator', render: text => <strong>{text}</strong> },
    { title: 'Department', dataIndex: 'department', key: 'department', render: dept => <Tag color="blue">{dept}</Tag> },
    { title: 'Current Value', dataIndex: 'value', key: 'value' },
    { title: 'Benchmark Target', dataIndex: 'target', key: 'target' },
    { 
      title: 'Target Progress', 
      key: 'progress', 
      render: (_, r) => (
        <Progress 
          percent={r.progress} 
          size="small" 
          status={r.status === 'Needs Attention' ? 'exception' : r.status === 'Exceeded' ? 'success' : 'active'}
        />
      ) 
    },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status', 
      render: status => {
        const color = status === 'Exceeded' ? 'green' : status === 'On Track' ? 'blue' : 'gold';
        return <Tag color={color}>{status}</Tag>;
      } 
    }
  ];

  const bottleneckColumns = [
    { title: 'Bottleneck / Issue', dataIndex: 'issue', key: 'issue', render: text => <strong>{text}</strong> },
    { title: 'Department', dataIndex: 'department', key: 'department', render: d => <Tag color="geekblue">{d}</Tag> },
    { title: 'Location', dataIndex: 'location', key: 'location' },
    { 
      title: 'Urgency', 
      dataIndex: 'urgency', 
      key: 'urgency', 
      render: u => <Tag color={u === 'Critical' ? 'red' : u === 'High' ? 'volcano' : 'orange'}>{u}</Tag> 
    },
    { title: 'Aging', dataIndex: 'aging', key: 'aging', render: a => <span style={{ color: '#cf1322' }}>{a}</span> },
    { title: 'SLA Limit', dataIndex: 'slaLimit', key: 'slaLimit' },
    { title: 'Assignee', dataIndex: 'owner', key: 'owner' },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Button 
          type="primary" 
          size="small" 
          danger={record.urgency === 'Critical'}
          onClick={() => message.success(`Urgent notification dispatched to ${record.owner}`)}
        >
          Escalate
        </Button>
      )
    }
  ];

  const tabItems = [
    {
      key: '1',
      label: 'Trend Analysis',
      children: (
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={16}>
            <Card title="Monthly SLA Compliance & Resolution Volume" extra={<Tag color="green">Last 6 Months</Tag>}>
              <div style={{ height: 320 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={monthlyTrends}>
                    <defs>
                      <linearGradient id="slaColor" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#1890ff" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#1890ff" stopOpacity={0.1}/>
                      </linearGradient>
                      <linearGradient id="resColor" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#52c41a" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#52c41a" stopOpacity={0.1}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="month" />
                    <YAxis yAxisId="left" domain={[70, 100]} unit="%" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip />
                    <Legend />
                    <Area yAxisId="left" type="monotone" dataKey="slaRate" name="SLA Compliance %" stroke="#1890ff" fill="url(#slaColor)" />
                    <Line yAxisId="right" type="monotone" dataKey="resolved" name="Cases Resolved" stroke="#52c41a" strokeWidth={3} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </Col>
          <Col xs={24} lg={8}>
            <Card title="Citizen Satisfaction Rating" extra={<Tag color="blue">District Survey</Tag>}>
              <div style={{ height: 320 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={monthlyTrends}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="month" />
                    <YAxis domain={[3.5, 5]} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="satisfaction" name="Rating (out of 5)" stroke="#722ed1" strokeWidth={3} dot={{ r: 6 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </Col>
        </Row>
      )
    },
    {
      key: '2',
      label: 'Department Comparison',
      children: (
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={15}>
            <Card title="Target vs Actual Service Case Throughput">
              <div style={{ height: 340 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={filteredComparison}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="department" tick={{ fontSize: 11 }} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="target" name="Monthly Target" fill="#d9d9d9" />
                    <Bar dataKey="actual" name="Actual Resolved" fill="#1890ff" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </Col>
          <Col xs={24} lg={9}>
            <Card title="Workload Distribution Across Units">
              <div style={{ height: 340 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie data={departmentWorkloadPie} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={95} label>
                      {departmentWorkloadPie.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </Card>
          </Col>
        </Row>
      )
    },
    {
      key: '3',
      label: 'Key Performance Indicators',
      children: (
        <Card title="District Governance Scorecard">
          <Table dataSource={filteredKpi} columns={kpiColumns} pagination={false} size="middle" />
        </Card>
      )
    },
    {
      key: '4',
      label: 'SLA Bottlenecks & Escalations',
      children: (
        <Card 
          title="Active SLA Threshold Breaches" 
          extra={<Button icon={<ReloadOutlined />} onClick={() => message.info('Refreshed latest sensor and ticket telemetry')}>Refresh Telemetry</Button>}
        >
          <Table dataSource={bottleneckData} columns={bottleneckColumns} pagination={{ pageSize: 5 }} size="middle" />
        </Card>
      )
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>Performance Metrics & SLA Analytics</h1>
          <span style={{ color: '#8c8c8c' }}>District-wide operational throughput, service delivery benchmarks, and bottlenecks</span>
        </div>
        <Space>
          <Select value={selectedDept} onChange={setSelectedDept} style={{ width: 200 }}>
            <Option value="All">All Departments</Option>
            {departmentComparison.map(d => <Option key={d.department} value={d.department}>{d.department}</Option>)}
          </Select>
          <RangePicker />
        </Space>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed', borderColor: '#b7eb8f' }}>
            <Statistic
              title="Overall SLA Compliance"
              value={94.8}
              precision={1}
              suffix="%"
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#389e0d', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>
              <RiseOutlined /> +2.4% vs previous month
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#e6f7ff', borderColor: '#91d5ff' }}>
            <Statistic
              title="Avg Case Resolution Time"
              value={4.6}
              precision={1}
              suffix="hrs"
              prefix={<ClockCircleOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#096dd9', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>
              <FallOutlined /> -1.2 hrs faster turnaround
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f9f0ff', borderColor: '#d3adf7' }}>
            <Statistic
              title="Citizen Satisfaction Index"
              value={4.7}
              precision={1}
              suffix="/ 5.0"
              prefix={<DashboardOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#531dab', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#722ed1' }}>
              94% positive grievance feedback
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fffbe6', borderColor: '#ffe58f' }}>
            <Statistic
              title="Cases Resolved (MTD)"
              value={2049}
              prefix={<RiseOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#d48806', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#d48806' }}>
              4 active bottleneck escalations
            </div>
          </Card>
        </Col>
      </Row>

      <Tabs activeKey={activeTab} onChange={setActiveTab} items={tabItems} />
    </div>
  );
};

export default PerformanceMetrics;
