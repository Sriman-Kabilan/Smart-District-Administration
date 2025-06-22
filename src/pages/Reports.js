import React, { useState } from 'react';
import { Card, Row, Col, Button, Select, DatePicker, Table, Tabs, Form, Input, Checkbox, Alert, Space, Tag, Progress } from 'antd';
import { DownloadOutlined, FileExcelOutlined, FilePdfOutlined, BarChartOutlined, CalendarOutlined, FilterOutlined } from '@ant-design/icons';

const { Option } = Select;
const { RangePicker } = DatePicker;
const { TabPane } = Tabs;

const Reports = () => {
  const [selectedReport, setSelectedReport] = useState('performance');
  const [dateRange, setDateRange] = useState(null);
  const [selectedDepartments, setSelectedDepartments] = useState([]);
  const [form] = Form.useForm();

  const departments = ['Public Works', 'Health', 'Education', 'Finance', 'Transportation', 'Environment', 'Social Services', 'Planning', 'Legal', 'IT'];
  
  const reportTypes = [
    { value: 'performance', label: 'Performance Summary Report' },
    { value: 'budget', label: 'Budget Analysis Report' },
    { value: 'tasks', label: 'Task Completion Report' },
    { value: 'resource', label: 'Resource Utilization Report' },
    { value: 'citizen', label: 'Citizen Satisfaction Report' },
    { value: 'compliance', label: 'Compliance & Audit Report' },
    { value: 'custom', label: 'Custom Analytics Report' }
  ];

  const scheduledColumns = [
    { title: 'Report Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'type', key: 'type' },
    { title: 'Schedule', dataIndex: 'schedule', key: 'schedule' },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (status) => <Tag color={status === 'Active' ? 'green' : 'orange'}>{status}</Tag> },
    { title: 'Last Generated', dataIndex: 'lastGenerated', key: 'lastGenerated' },
    { title: 'Recipients', dataIndex: 'recipients', key: 'recipients' },
    { title: 'Actions', key: 'actions', render: () => <Space><Button size="small">Edit</Button><Button size="small">Run Now</Button></Space> }
  ];

  const recentColumns = [
    { title: 'Report Name', dataIndex: 'name', key: 'name' },
    { title: 'Type', dataIndex: 'type', key: 'type' },
    { title: 'Generated', dataIndex: 'generated', key: 'generated' },
    { title: 'Size', dataIndex: 'size', key: 'size' },
    { title: 'Format', dataIndex: 'format', key: 'format', render: (format) => <Tag>{format}</Tag> },
    { title: 'Downloads', dataIndex: 'downloads', key: 'downloads' },
    { title: 'Actions', key: 'actions', render: () => <Space><Button size="small" icon={<DownloadOutlined />}>Download</Button><Button size="small">Share</Button></Space> }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Reports & Analytics</h1>
        <Space>
          <Button type="primary" icon={<BarChartOutlined />}>Generate Report</Button>
          <Button icon={<CalendarOutlined />}>Schedule Report</Button>
        </Space>
      </div>

      <Alert
        message="Reporting System"
        description="Connect to your district data sources for comprehensive report generation and automated distribution capabilities."
        type="info"
        showIcon
        style={{ marginBottom: '24px' }}
      />

      <Tabs defaultActiveKey="1">
        <TabPane tab="Generate Reports" key="1">
          <Row gutter={16}>
            <Col span={8}>
              <Card title="Report Configuration">
                <Form form={form} layout="vertical">
                  <Form.Item label="Report Type" name="reportType">
                    <Select placeholder="Select report type" value={selectedReport} onChange={setSelectedReport}>
                      {reportTypes.map(type => <Option key={type.value} value={type.value}>{type.label}</Option>)}
                    </Select>
                  </Form.Item>
                  
                  <Form.Item label="Date Range" name="dateRange">
                    <RangePicker style={{ width: '100%' }} onChange={setDateRange} />
                  </Form.Item>
                  
                  <Form.Item label="Departments" name="departments">
                    <Select mode="multiple" placeholder="Select departments" value={selectedDepartments} onChange={setSelectedDepartments}>
                      {departments.map(dept => <Option key={dept} value={dept}>{dept}</Option>)}
                    </Select>
                  </Form.Item>
                  
                  <Form.Item label="Output Format" name="format">
                    <Checkbox.Group>
                      <Checkbox value="pdf">PDF</Checkbox>
                      <Checkbox value="excel">Excel</Checkbox>
                      <Checkbox value="csv">CSV</Checkbox>
                    </Checkbox.Group>
                  </Form.Item>
                  
                  <Form.Item label="Include Visualizations" name="includeCharts">
                    <Checkbox>Include charts and graphs</Checkbox>
                  </Form.Item>
                  
                  <Form.Item label="Email Recipients" name="recipients">
                    <Input.TextArea rows={3} placeholder="Enter email addresses separated by commas" />
                  </Form.Item>
                </Form>
              </Card>
            </Col>
            
            <Col span={16}>
              <Card title="Report Preview">
                <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
                  <BarChartOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
                  <div>Report preview will be displayed here</div>
                  <div style={{ fontSize: '12px', marginTop: '8px' }}>Configure report settings and connect to data sources to generate preview</div>
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Scheduled Reports" key="2">
          <Card title="Automated Report Schedule">
            <Table dataSource={[]} columns={scheduledColumns} pagination={false} locale={{ emptyText: 'No scheduled reports configured' }} />
          </Card>
        </TabPane>

        <TabPane tab="Recent Reports" key="3">
          <Card title="Generated Reports Archive">
            <Table dataSource={[]} columns={recentColumns} pagination={{ pageSize: 10 }} locale={{ emptyText: 'No reports generated yet' }} />
          </Card>
        </TabPane>

        <TabPane tab="Analytics Dashboard" key="4">
          <Row gutter={16}>
            <Col span={12}>
              <Card title="Report Generation Trends">
                <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Report generation analytics will display here
                </div>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="Popular Reports">
                <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Most requested reports analysis will display here
                </div>
              </Card>
            </Col>
          </Row>
          
          <Row gutter={16} style={{ marginTop: '16px' }}>
            <Col span={8}>
              <Card title="Export Statistics">
                <div style={{ textAlign: 'center', padding: '20px' }}>
                  <Progress type="circle" percent={0} format={() => '0'} />
                  <div style={{ marginTop: '12px', color: '#666' }}>Reports Generated This Month</div>
                </div>
              </Card>
            </Col>
            <Col span={8}>
              <Card title="Format Distribution">
                <div style={{ height: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Format usage chart will display here
                </div>
              </Card>
            </Col>
            <Col span={8}>
              <Card title="Department Usage">
                <div style={{ height: '200px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Department report usage will display here
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Data Export" key="5">
          <Row gutter={16}>
            <Col span={12}>
              <Card title="Bulk Data Export">
                <Form layout="vertical">
                  <Form.Item label="Data Source">
                    <Select placeholder="Select data source">
                      <Option value="tasks">Task Management Data</Option>
                      <Option value="performance">Performance Metrics</Option>
                      <Option value="budget">Budget Information</Option>
                      <Option value="staff">Staff Records</Option>
                      <Option value="citizens">Citizen Services</Option>
                    </Select>
                  </Form.Item>
                  
                  <Form.Item label="Export Format">
                    <Select placeholder="Select format">
                      <Option value="csv">CSV</Option>
                      <Option value="excel">Excel</Option>
                      <Option value="json">JSON</Option>
                      <Option value="xml">XML</Option>
                    </Select>
                  </Form.Item>
                  
                  <Form.Item label="Date Range">
                    <RangePicker style={{ width: '100%' }} />
                  </Form.Item>
                  
                  <Button type="primary" icon={<DownloadOutlined />} block>Export Data</Button>
                </Form>
              </Card>
            </Col>
            
            <Col span={12}>
              <Card title="API Access">
                <div style={{ padding: '20px' }}>
                  <Alert message="Data API Integration" description="Connect to district data APIs for real-time data access and automated report generation." type="info" style={{ marginBottom: '16px' }} />
                  
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <Button block icon={<FileExcelOutlined />}>Download API Documentation</Button>
                    <Button block icon={<FilterOutlined />}>Configure Data Filters</Button>
                    <Button block>Test API Connection</Button>
                  </Space>
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default Reports;