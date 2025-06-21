import React, { useState } from 'react';
import { Card, Row, Col, Table, Button, Modal, Form, Input, Select, InputNumber, Tabs, Progress, Statistic, Alert, Tag, Space } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, DollarOutlined, TeamOutlined, ToolOutlined } from '@ant-design/icons';
import { PieChart, Pie, Cell, BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const { Option } = Select;
const { TabPane } = Tabs;

const ResourceManagement = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [editingResource, setEditingResource] = useState(null);
  const [form] = Form.useForm();

  const departments = ['Public Works', 'Health', 'Education', 'Finance', 'Transportation', 'Environment', 'Social Services', 'Planning', 'Legal', 'IT'];
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d'];

  const budgetColumns = [
    { title: 'Department', dataIndex: 'department', key: 'department' },
    { title: 'Allocated Budget', dataIndex: 'allocated', key: 'allocated', render: (amount) => `$${amount?.toLocaleString() || 0}` },
    { title: 'Spent', dataIndex: 'spent', key: 'spent', render: (amount) => `$${amount?.toLocaleString() || 0}` },
    { title: 'Remaining', dataIndex: 'remaining', key: 'remaining', render: (amount) => `$${amount?.toLocaleString() || 0}` },
    { title: 'Utilization', dataIndex: 'utilization', key: 'utilization', render: (percent) => <Progress percent={percent || 0} size="small" /> }
  ];

  const equipmentColumns = [
    { title: 'Equipment', dataIndex: 'name', key: 'name' },
    { title: 'Department', dataIndex: 'department', key: 'department' },
    { title: 'Quantity', dataIndex: 'quantity', key: 'quantity' },
    { title: 'Total Cost', dataIndex: 'cost', key: 'cost', render: (cost) => `$${cost?.toLocaleString() || 0}` },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (status) => <Tag color="green">{status || 'Active'}</Tag> },
    { title: 'Next Maintenance', dataIndex: 'nextMaintenance', key: 'nextMaintenance' },
    { title: 'Actions', key: 'actions', render: () => <Space><Button size="small" icon={<EditOutlined />} /><Button size="small" danger icon={<DeleteOutlined />} /></Space> }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Resource Management</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setModalVisible(true)}>
          Add Resource
        </Button>
      </div>

      <Alert
        message="Resource Management System"
        description="Connect to your financial and HR systems to manage budgets, staff allocations, and equipment across departments."
        type="info"
        showIcon
        style={{ marginBottom: '24px' }}
      />

      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic title="Total Budget" value={0} precision={0} prefix={<DollarOutlined />} formatter={(value) => `$${value.toLocaleString()}`} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Total Staff" value={0} prefix={<TeamOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Equipment Items" value={0} prefix={<ToolOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="Avg Utilization" value={0} precision={1} suffix="%" />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="1">
        <TabPane tab="Budget Management" key="1">
          <Row gutter={16}>
            <Col span={16}>
              <Card title="Budget Allocation by Department">
                <Table dataSource={[]} columns={budgetColumns} pagination={false} size="small" locale={{ emptyText: 'Connect to financial system to view budget data' }} />
              </Card>
            </Col>
            <Col span={8}>
              <Card title="Budget Distribution">
                <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Budget distribution chart will display here
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Staff Allocation" key="2">
          <Card title="Staff Distribution Across Departments">
            <div style={{ height: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
              Staff allocation charts will display here
            </div>
          </Card>
        </TabPane>

        <TabPane tab="Equipment & Assets" key="3">
          <Card title="Equipment Inventory">
            <Table dataSource={[]} columns={equipmentColumns} pagination={{ pageSize: 10 }} locale={{ emptyText: 'Connect to asset management system to view equipment data' }} />
          </Card>
        </TabPane>

        <TabPane tab="Resource Optimization" key="4">
          <Row gutter={16}>
            <Col span={12}>
              <Card title="Budget Utilization Trends">
                <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666' }}>
                  Budget utilization trends will display here
                </div>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="Optimization Recommendations">
                <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>
                  AI-powered optimization recommendations will appear here when connected to your systems
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>
      </Tabs>

      <Modal title="Add New Resource" open={modalVisible} onCancel={() => setModalVisible(false)} footer={null} width={600}>
        <Form form={form} layout="vertical">
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item label="Equipment Name" name="name" rules={[{ required: true, message: 'Please enter equipment name' }]}>
                <Input />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item label="Department" name="department" rules={[{ required: true, message: 'Please select department' }]}>
                <Select>{departments.map(dept => <Option key={dept} value={dept}>{dept}</Option>)}</Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item label="Quantity" name="quantity" rules={[{ required: true, message: 'Please enter quantity' }]}>
                <InputNumber min={1} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item label="Total Cost" name="cost" rules={[{ required: true, message: 'Please enter cost' }]}>
                <InputNumber min={0} formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')} parser={value => value.replace(/\$\s?|(,*)/g, '')} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item label="Next Maintenance Date" name="nextMaintenance">
            <Input type="date" />
          </Form.Item>
          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Button onClick={() => setModalVisible(false)} style={{ marginRight: 8 }}>Cancel</Button>
            <Button type="primary" htmlType="submit">Add Resource</Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ResourceManagement;