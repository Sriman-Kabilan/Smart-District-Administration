import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Spin, Select, Alert } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';

const { Option } = Select;

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [selectedDepartment, setSelectedDepartment] = useState(null);

  // Mock data for demonstration - in real app, fetch from API
  const mockData = {
    administrator: {
      total_departments: 7,
      active_tasks: 142,
      total_staff: 89,
      budget_utilization: 78.3,
      task_change_percent: 12.5,
    },
    department_head: {
      department_tasks: 24,
      completion_rate: 87.5,
      team_members: 12,
      efficiency_score: 92.1,
      task_change_percent: 8.3,
    },
    staff: {
      my_tasks: 8,
      completed_week: 5,
      pending_tasks: 3,
    }
  };

  const data = mockData[user?.role] || mockData.staff;

  const renderAdminDashboard = () => (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Departments"
              value={data.total_departments}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Active Tasks"
              value={data.active_tasks}
              valueStyle={{ color: '#52c41a' }}
              prefix={<ArrowUpOutlined />}
              suffix={`+${data.task_change_percent}%`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Staff"
              value={data.total_staff}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Budget Utilization"
              value={data.budget_utilization}
              precision={1}
              suffix="%"
              valueStyle={{ color: '#fa8c16' }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="Performance Overview">
            <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
              Performance charts will be displayed here
            </div>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Resource Allocation">
            <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
              Resource allocation charts will be displayed here
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );

  const renderDepartmentHeadDashboard = () => (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Department Tasks"
              value={data.department_tasks}
              valueStyle={{ color: '#1890ff' }}
              prefix={<ArrowUpOutlined />}
              suffix={`+${data.task_change_percent}%`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Completion Rate"
              value={data.completion_rate}
              precision={1}
              suffix="%"
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Team Members"
              value={data.team_members}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Efficiency Score"
              value={data.efficiency_score}
              precision={1}
              valueStyle={{ color: '#fa8c16' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="Department Performance">
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          Department performance metrics will be displayed here
        </div>
      </Card>
    </div>
  );

  const renderStaffDashboard = () => (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="My Tasks"
              value={data.my_tasks}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="Completed This Week"
              value={data.completed_week}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="Pending Tasks"
              value={data.pending_tasks}
              valueStyle={{ color: '#fa541c' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="My Recent Tasks">
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          Your assigned tasks will be displayed here
        </div>
      </Card>
    </div>
  );

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div>
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        {user?.role === 'administrator' && (
          <Select
            placeholder="Select Department"
            style={{ width: 200 }}
            allowClear
            value={selectedDepartment}
            onChange={setSelectedDepartment}
          >
            <Option value="Public Works">Public Works</Option>
            <Option value="Education">Education</Option>
            <Option value="Health">Health</Option>
            <Option value="Finance">Finance</Option>
            <Option value="Urban Planning">Urban Planning</Option>
            <Option value="Transportation">Transportation</Option>
            <Option value="Social Services">Social Services</Option>
          </Select>
        )}
      </div>

      <Alert
        message="Demo Mode"
        description="This is a demonstration with sample data. In production, real-time data would be displayed here."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      {user?.role === 'administrator' && renderAdminDashboard()}
      {user?.role === 'department_head' && renderDepartmentHeadDashboard()}
      {user?.role === 'staff' && renderStaffDashboard()}
    </div>
  );
};

export default Dashboard;