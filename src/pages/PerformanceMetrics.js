import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Select, DatePicker, Table, Progress, Tabs, Alert } from 'antd';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { TrendingUpOutlined, TrendingDownOutlined, DashboardOutlined } from '@ant-design/icons';
import { dashboardService } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

const { Option } = Select;
const { RangePicker } = DatePicker;
const { TabPane } = Tabs;

const PerformanceMetrics = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [dateRange, setDateRange] = useState(null);
  const [performanceData, setPerformanceData] = useState(null);

  useEffect(() => {
    loadPerformanceData();
  }, [selectedDepartment, dateRange]);

  const loadPerformanceData = async () => {
    try {
      setLoading(true);
      const data = await dashboardService.getPerformanceMetrics(selectedDepartment, dateRange);
      setPerformanceData(data);
    } catch (error) {
      console.error('Failed to load performance data:', error);
      setPerformanceData(null);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const departments = [
    'Public Works', 'Health', 'Education', 'Finance', 'Transportation', 
    'Environment', 'Social Services', 'Planning', 'Legal', 'IT'
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Performance Metrics & Analytics</h1>
        <div style={{ display: 'flex', gap: '16px' }}>
          <Select
            placeholder="Select Department"
            style={{ width: 200 }}
            allowClear
            value={selectedDepartment}
            onChange={setSelectedDepartment}
          >
            {departments.map(dept => (
              <Option key={dept} value={dept}>{dept}</Option>
            ))}
          </Select>
          <RangePicker onChange={setDateRange} />
        </div>
      </div>

      <Alert
        message="Performance Analytics"
        description="Connect to your district's performance management system to view real-time metrics. Current display shows system interface."
        type="info"
        showIcon
        style={{ marginBottom: '24px' }}
      />

      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Efficiency Rate"
              value={0}
              precision={1}
              suffix="%"
              prefix={<DashboardOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
            <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
              Awaiting data connection
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Budget Utilization"
              value={0}
              precision={1}
              suffix="%"
              prefix={<DashboardOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
            <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
              Awaiting data connection
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Citizen Satisfaction"
              value={0}
              precision={1}
              suffix="%"
              prefix={<DashboardOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
            <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
              Awaiting data connection
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Task Completion Rate"
              value={0}
              precision={1}
              suffix="%"
              prefix={<DashboardOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
            <div style={{ marginTop: '8px', fontSize: '12px', color: '#666' }}>
              Awaiting data connection
            </div>
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="1">
        <TabPane tab="Trend Analysis" key="1">
          <Row gutter={16}>
            <Col span={24}>
              <Card title="Performance Trends Over Time" loading={loading}>
                <div style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Connect your analytics system to display performance trend charts
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Department Comparison" key="2">
          <Row gutter={16}>
            <Col span={12}>
              <Card title="Efficiency by Department" loading={loading}>
                <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Department efficiency comparison charts
                </div>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="Budget Utilization by Department" loading={loading}>
                <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Budget utilization visualization
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Key Performance Indicators" key="3">
          <Card title="Performance Indicators Dashboard" loading={loading}>
            <Table
              dataSource={[]}
              columns={[
                { title: 'Indicator', dataIndex: 'name', key: 'name' },
                { title: 'Current', dataIndex: 'value', key: 'value' },
                { title: 'Target', dataIndex: 'target', key: 'target' },
                { title: 'Progress', key: 'progress', render: () => <Progress percent={0} size="small" /> },
                { title: 'Status', dataIndex: 'status', key: 'status' }
              ]}
              locale={{ emptyText: 'Connect data source to view KPI metrics' }}
              pagination={false}
              size="small"
            />
          </Card>
        </TabPane>

        <TabPane tab="Satisfaction Analysis" key="4">
          <Row gutter={16}>
            <Col span={24}>
              <Card title="Citizen Satisfaction Trends" loading={loading}>
                <div style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Citizen satisfaction trend analysis will display here
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default PerformanceMetrics;