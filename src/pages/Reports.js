import React, { useState } from 'react';
import { 
  Card, Row, Col, Button, Select, DatePicker, Table, Tabs, 
  Tag, Space, Progress, Statistic, message, Modal, Form, Input, Badge 
} from 'antd';
import { 
  DownloadOutlined, FilePdfOutlined, FileExcelOutlined, 
  PrinterOutlined, CalendarOutlined, PlusOutlined, CheckCircleOutlined, 
  FileTextOutlined, ClockCircleOutlined 
} from '@ant-design/icons';

const { Option } = Select;
const { RangePicker } = DatePicker;

// Sample Compiled Report Datasets for Live Preview
const samplePerformanceReport = [
  { key: '1', metric: 'SLA Target Compliance Rate', category: 'Operational', q1: '91.2%', q2: '93.5%', q3: '94.8%', status: 'Exceeded' },
  { key: '2', metric: 'Average Grievance Resolution Time', category: 'Public Service', q1: '6.2 hrs', q2: '5.4 hrs', q3: '4.6 hrs', status: 'On Track' },
  { key: '3', metric: 'Clean Drinking Water Compliance', category: 'Health & Sanitation', q1: '98.7%', q2: '99.1%', q3: '99.4%', status: 'Exceeded' },
  { key: '4', metric: 'Pothole Restoration Turnaround', category: 'Civil Works', q1: '54 hrs', q2: '46 hrs', q3: '42 hrs', status: 'On Track' },
  { key: '5', metric: 'Property Tax Collection Target', category: 'Revenue & Finance', q1: '74.2%', q2: '79.0%', q3: '82.6%', status: 'Exceeded' },
  { key: '6', metric: 'Public Bus Schedule Punctuality', category: 'Transportation', q1: '72.0%', q2: '75.5%', q3: '78.2%', status: 'Needs Attention' }
];

const initialScheduledReports = [
  {
    key: '1',
    name: 'Weekly District Magistrate Executive Summary',
    type: 'Comprehensive Digest',
    frequency: 'Weekly (Every Monday 08:00 AM)',
    recipients: 'magistrate@district.gov, dept_heads@district.gov',
    lastGenerated: '2026-11-09',
    status: 'Active'
  },
  {
    key: '2',
    name: 'Monthly Treasury & Budget Utilization Audit',
    type: 'Financial Audit',
    frequency: 'Monthly (1st of Month)',
    recipients: 'finance@district.gov, auditor@state.gov',
    lastGenerated: '2026-11-01',
    status: 'Active'
  },
  {
    key: '3',
    name: 'Daily Citizen Grievance Escalation Digest',
    type: 'SLA Redressal',
    frequency: 'Daily (Every Evening 18:00 PM)',
    recipients: 'sla_cell@district.gov',
    lastGenerated: '2026-11-09',
    status: 'Active'
  }
];

const Reports = () => {
  const [reportType, setReportType] = useState('performance');
  const [selectedDept, setSelectedDept] = useState('All');
  const [scheduledReports, setScheduledReports] = useState(initialScheduledReports);
  const [scheduleModalOpen, setScheduleModalOpen] = useState(false);
  const [form] = Form.useForm();

  // CSV Export utility
  const handleExportCSV = () => {
    const headers = ['Performance Metric', 'Category', 'Q1 Benchmark', 'Q2 Benchmark', 'Q3 Current', 'Status'];
    const rows = samplePerformanceReport.map(r => [
      `"${r.metric}"`,
      `"${r.category}"`,
      `"${r.q1}"`,
      `"${r.q2}"`,
      `"${r.q3}"`,
      `"${r.status}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `District_Report_${reportType}_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    message.success('CSV dataset exported successfully.');
  };

  const handlePrintPDF = () => {
    window.print();
  };

  const handleAddSchedule = (values) => {
    const newSchedule = {
      key: `${Date.now()}`,
      name: values.name,
      type: values.type,
      frequency: values.frequency,
      recipients: values.recipients,
      lastGenerated: 'Pending Next Cycle',
      status: 'Active'
    };
    setScheduledReports([...scheduledReports, newSchedule]);
    message.success('Automated dispatch schedule registered.');
    setScheduleModalOpen(false);
    form.resetFields();
  };

  const previewColumns = [
    { title: 'Governance Indicator / Metric', dataIndex: 'metric', key: 'metric', render: t => <strong>{t}</strong> },
    { title: 'Sector / Category', dataIndex: 'category', key: 'category', render: c => <Tag color="blue">{c}</Tag> },
    { title: 'Q1 2026', dataIndex: 'q1', key: 'q1' },
    { title: 'Q2 2026', dataIndex: 'q2', key: 'q2' },
    { title: 'Q3 2026 (Current)', dataIndex: 'q3', key: 'q3', render: q => <strong style={{ color: '#1890ff' }}>{q}</strong> },
    { 
      title: 'Audit Assessment', 
      dataIndex: 'status', 
      key: 'status',
      render: st => {
        const color = st === 'Exceeded' ? 'green' : st === 'On Track' ? 'blue' : 'orange';
        return <Tag color={color}>{st}</Tag>;
      }
    }
  ];

  const scheduledColumns = [
    { title: 'Report Title', dataIndex: 'name', key: 'name', render: t => <strong>{t}</strong> },
    { title: 'Report Classification', dataIndex: 'type', key: 'type', render: tp => <Tag color="geekblue">{tp}</Tag> },
    { title: 'Automated Cadence', dataIndex: 'frequency', key: 'frequency' },
    { title: 'Target Distribution List', dataIndex: 'recipients', key: 'recipients' },
    { title: 'Last Dispatched', dataIndex: 'lastGenerated', key: 'lastGenerated' },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: s => <Tag color="green" icon={<CheckCircleOutlined />}>{s}</Tag>
    }
  ];

  const tabItems = [
    {
      key: '1',
      label: 'Compiled Report Preview',
      children: (
        <Card 
          title={`Compiled Live Digest: ${reportType.toUpperCase()} OVERVIEW`}
          extra={
            <Space>
              <Button icon={<FileExcelOutlined />} onClick={handleExportCSV}>Export CSV</Button>
              <Button type="primary" icon={<PrinterOutlined />} onClick={handlePrintPDF}>Print / PDF</Button>
            </Space>
          }
        >
          <div style={{ marginBottom: 16, background: '#fafafa', padding: 12, borderRadius: 6, display: 'flex', justifyContent: 'space-between' }}>
            <span><strong>District Scope:</strong> {selectedDept}</span>
            <span><strong>Audit Period:</strong> Fiscal Year 2026-27 (Q1 - Q3)</span>
            <span><strong>Compliance Seal:</strong> Verified Cryptographic Signature</span>
          </div>
          <Table dataSource={samplePerformanceReport} columns={previewColumns} pagination={false} size="middle" />
        </Card>
      )
    },
    {
      key: '2',
      label: 'Automated Scheduled Dispatches',
      children: (
        <Card 
          title="Automated PDF & CSV Report Pipeline"
          extra={<Button type="primary" icon={<PlusOutlined />} onClick={() => setScheduleModalOpen(true)}>Create Recurring Schedule</Button>}
        >
          <Table dataSource={scheduledReports} columns={scheduledColumns} pagination={false} size="middle" />
        </Card>
      )
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>District Governance Reports & Auditing</h1>
          <span style={{ color: '#8c8c8c' }}>Official executive digests, statutory audit compliance, and scheduled telemetry exports</span>
        </div>
        <Space wrap>
          <Select value={reportType} onChange={setReportType} style={{ width: 240 }}>
            <Option value="performance">📊 District Performance Digest</Option>
            <Option value="financial">💰 Financial & Budget Audit</Option>
            <Option value="grievances">⚠️ Grievance SLA Compliance</Option>
            <Option value="assets">🚜 Capital Assets & Equipment</Option>
          </Select>
          <Select value={selectedDept} onChange={setSelectedDept} style={{ width: 180 }}>
            <Option value="All">All Departments</Option>
            <Option value="Public Works">Public Works</Option>
            <Option value="Health & Sanitation">Health & Sanitation</Option>
            <Option value="Transportation">Transportation</Option>
          </Select>
          <RangePicker />
        </Space>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f0f5ff', borderColor: '#adc6ff' }}>
            <Statistic
              title="Official Reports Compiled"
              value={142}
              suffix="documents"
              prefix={<FileTextOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1d39c4', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>Fiscal Year archive complete</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed', borderColor: '#b7eb8f' }}>
            <Statistic
              title="Statutory Audit Readiness"
              value={100}
              suffix="%"
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#389e0d', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>All ledgers reconciled</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff7e6', borderColor: '#ffd591' }}>
            <Statistic
              title="Active Scheduled Subscriptions"
              value={scheduledReports.length}
              suffix="pipelines"
              prefix={<ClockCircleOutlined style={{ color: '#fa8c16' }} />}
              valueStyle={{ color: '#d46b08', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#fa8c16' }}>Daily & Weekly digests</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f9f0ff', borderColor: '#d3adf7' }}>
            <Statistic
              title="Transparency Index"
              value={98.2}
              precision={1}
              suffix="%"
              prefix={<CalendarOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#531dab', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#722ed1' }}>Public portal publication SLA</div>
          </Card>
        </Col>
      </Row>

      <Tabs activeKey={tabItems[0].key} items={tabItems} />

      <Modal
        title="Schedule Automated Recurring Report"
        open={scheduleModalOpen}
        onCancel={() => setScheduleModalOpen(false)}
        footer={null}
      >
        <Form form={form} layout="vertical" onFinish={handleAddSchedule}>
          <Form.Item name="name" label="Schedule Name" rules={[{ required: true, message: 'Please input schedule name' }]}>
            <Input placeholder="e.g. Bi-Weekly Sanitation SLA Audit" />
          </Form.Item>
          <Form.Item name="type" label="Report Category" initialValue="Comprehensive Digest">
            <Select>
              <Option value="Comprehensive Digest">Comprehensive Digest</Option>
              <Option value="Financial Audit">Financial Audit</Option>
              <Option value="SLA Redressal">SLA Redressal</Option>
              <Option value="Capital Assets">Capital Assets</Option>
            </Select>
          </Form.Item>
          <Form.Item name="frequency" label="Cadence" initialValue="Weekly (Every Monday)">
            <Select>
              <Option value="Daily (08:00 AM)">Daily (08:00 AM)</Option>
              <Option value="Weekly (Every Monday)">Weekly (Every Monday)</Option>
              <Option value="Monthly (1st Day)">Monthly (1st Day)</Option>
            </Select>
          </Form.Item>
          <Form.Item name="recipients" label="Recipient Email Addresses" rules={[{ required: true, message: 'Please specify recipient emails' }]}>
            <Input placeholder="magistrate@district.gov, secretary@district.gov" />
          </Form.Item>
          <div style={{ textAlign: 'right', marginTop: 16 }}>
            <Space>
              <Button onClick={() => setScheduleModalOpen(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit">Save Automation</Button>
            </Space>
          </div>
        </Form>
      </Modal>
    </div>
  );
};

export default Reports;
