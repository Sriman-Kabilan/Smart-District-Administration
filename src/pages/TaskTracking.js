import React, { useState, useEffect } from 'react';
import { 
  Card, Button, Table, Tag, Space, Alert, Modal, Form, 
  Input, Select, DatePicker, Row, Col, Statistic, Popconfirm, 
  message, Dropdown, Menu 
} from 'antd';
import { 
  PlusOutlined, EditOutlined, DeleteOutlined, CheckCircleOutlined, 
  ClockCircleOutlined, AlertOutlined, DownOutlined, FilterOutlined 
} from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const { Option } = Select;
const { TextArea } = Input;

const initialDistrictTasks = [
  {
    id: '1',
    task_id: 'T-001',
    task_name: 'Road Maintenance Survey & Pothole Tagging',
    description: 'Conduct comprehensive survey of arterial roads in Ward 2',
    priority: 'High',
    status: 'In Progress',
    assigned_to: 'staff',
    due_date: '2026-11-20',
    department: 'Public Works',
  },
  {
    id: '2',
    task_id: 'T-002',
    task_name: 'Quarterly Municipal Budget Reconciliation',
    description: 'Prepare expenditure reconciliation for Q3 audit',
    priority: 'Medium',
    status: 'Pending',
    assigned_to: 'dept_head',
    due_date: '2026-11-25',
    department: 'Revenue & Finance',
  },
  {
    id: '3',
    task_id: 'T-003',
    task_name: 'Primary School Drinking Water Testing',
    description: 'Sample testing across 12 civic schools',
    priority: 'Critical',
    status: 'Completed',
    assigned_to: 'staff',
    due_date: '2026-11-10',
    department: 'Health & Sanitation',
  },
  {
    id: '4',
    task_id: 'T-004',
    task_name: 'Traffic Signal Sensor Synchronization',
    description: 'Deploy firmware update to automated signal controllers',
    priority: 'High',
    status: 'In Progress',
    assigned_to: 'staff',
    due_date: '2026-11-18',
    department: 'Transportation',
  },
  {
    id: '5',
    task_id: 'T-005',
    task_name: 'Solar Panel Maintenance at Civic Center Block B',
    description: 'Routine inverter diagnostic and panel cleaning',
    priority: 'Low',
    status: 'Pending',
    assigned_to: 'staff',
    due_date: '2026-11-30',
    department: 'Public Works',
  }
];

const TaskTracking = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState(initialDistrictTasks);
  const [loading, setLoading] = useState(false);
  const [selectedDept, setSelectedDept] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [form] = Form.useForm();

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const res = await api.get('/tasks');
      if (res.data && Array.isArray(res.data) && res.data.length > 0) {
        setTasks(res.data);
      }
    } catch (err) {
      // Fallback to local state if backend is booting
      console.log('Using local task dataset');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleCreateOrUpdateTask = async (values) => {
    const formattedDueDate = values.due_date 
      ? values.due_date.format('YYYY-MM-DD') 
      : '2026-12-01';

    if (editingTask) {
      // Update existing
      const updated = tasks.map(t => t.id === editingTask.id ? {
        ...t,
        task_name: values.task_name,
        department: values.department,
        priority: values.priority,
        assigned_to: values.assigned_to,
        due_date: formattedDueDate,
        description: values.description
      } : t);
      setTasks(updated);
      message.success(`Task ${editingTask.task_id} updated.`);
    } else {
      // Create new
      const newId = `T-${String(tasks.length + 1).padStart(3, '0')}`;
      const newTask = {
        id: `${Date.now()}`,
        task_id: newId,
        task_name: values.task_name,
        description: values.description || '',
        priority: values.priority,
        status: 'Pending',
        assigned_to: values.assigned_to || user?.username || 'staff',
        due_date: formattedDueDate,
        department: values.department,
      };

      try {
        await api.post('/tasks', newTask);
      } catch (e) {
        // Fallback locally
      }
      setTasks([newTask, ...tasks]);
      message.success(`Task ${newId} created successfully.`);
    }

    setIsModalOpen(false);
    setEditingTask(null);
    form.resetFields();
  };

  const handleStatusChange = async (taskId, newStatus) => {
    setTasks(tasks.map(t => t.task_id === taskId || t.id === taskId ? { ...t, status: newStatus } : t));
    try {
      await api.patch(`/tasks/${taskId}/status`, { status: newStatus });
    } catch (e) {
      // Local state already updated
    }
    message.success(`Task status updated to ${newStatus}`);
  };

  const handleDeleteTask = async (taskId) => {
    setTasks(tasks.filter(t => t.task_id !== taskId && t.id !== taskId));
    try {
      await api.delete(`/tasks/${taskId}`);
    } catch (e) {
      // Local state already updated
    }
    message.success('Task removed from dispatch queue.');
  };

  const openEditModal = (record) => {
    setEditingTask(record);
    form.setFieldsValue({
      task_name: record.task_name,
      department: record.department,
      priority: record.priority,
      assigned_to: record.assigned_to,
      description: record.description
    });
    setIsModalOpen(true);
  };

  const getPriorityColor = (priority) => {
    const colors = {
      'Low': 'green',
      'Medium': 'blue',
      'High': 'orange',
      'Critical': 'red',
    };
    return colors[priority] || 'default';
  };

  const getStatusColor = (status) => {
    const colors = {
      'Pending': 'orange',
      'In Progress': 'blue',
      'Completed': 'green',
      'Canceled': 'red',
    };
    return colors[status] || 'default';
  };

  // Filter tasks based on role and selected filters
  const filteredTasks = tasks.filter(task => {
    if (user?.role === 'staff' && task.assigned_to !== user.username) return false;
    if (user?.role === 'department_head' && task.department !== user.department) return false;
    if (selectedDept !== 'All' && task.department !== selectedDept) return false;
    if (selectedStatus !== 'All' && task.status !== selectedStatus) return false;
    return true;
  });

  const columns = [
    {
      title: 'Task ID',
      dataIndex: 'task_id',
      key: 'task_id',
      render: id => <Tag color="geekblue">{id}</Tag>
    },
    {
      title: 'Task Deliverable',
      dataIndex: 'task_name',
      key: 'task_name',
      render: (name, r) => (
        <div>
          <strong>{name}</strong>
          {r.description && <div style={{ fontSize: 12, color: '#8c8c8c' }}>{r.description}</div>}
        </div>
      )
    },
    {
      title: 'Department',
      dataIndex: 'department',
      key: 'department',
      render: d => <Tag color="blue">{d}</Tag>
    },
    {
      title: 'Assigned To',
      dataIndex: 'assigned_to',
      key: 'assigned_to',
      render: a => <Tag color="purple">{a}</Tag>
    },
    {
      title: 'Priority',
      dataIndex: 'priority',
      key: 'priority',
      render: priority => <Tag color={getPriorityColor(priority)}>{priority}</Tag>
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status, record) => {
        const statusItems = [
          { key: 'Pending', label: 'Pending' },
          { key: 'In Progress', label: 'In Progress' },
          { key: 'Completed', label: 'Completed' },
          { key: 'Canceled', label: 'Canceled' }
        ];

        return (
          <Dropdown
            menu={{
              items: statusItems,
              onClick: ({ key }) => handleStatusChange(record.task_id || record.id, key)
            }}
          >
            <Button size="small" style={{ borderColor: getStatusColor(status) }}>
              <Tag color={getStatusColor(status)} style={{ margin: 0 }}>{status}</Tag>
              <DownOutlined style={{ fontSize: 10, marginLeft: 4 }} />
            </Button>
          </Dropdown>
        );
      }
    },
    {
      title: 'Due Date',
      dataIndex: 'due_date',
      key: 'due_date',
      render: d => <span><ClockCircleOutlined style={{ marginRight: 4 }} />{d}</span>
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            type="text"
            icon={<EditOutlined />}
            onClick={() => openEditModal(record)}
          />
          {user?.role !== 'staff' && (
            <Popconfirm
              title="Delete Task"
              description="Are you sure you want to remove this task?"
              onConfirm={() => handleDeleteTask(record.task_id || record.id)}
              okText="Yes"
              cancelText="No"
            >
              <Button type="text" danger icon={<DeleteOutlined />} />
            </Popconfirm>
          )}
        </Space>
      )
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>District Task Tracking & Workflow Dispatch</h1>
          <span style={{ color: '#8c8c8c' }}>Assign, monitor, and resolve civic action deliverables across all administrative units</span>
        </div>
        <Space wrap>
          <Select value={selectedDept} onChange={setSelectedDept} style={{ width: 180 }}>
            <Option value="All">All Departments</Option>
            <Option value="Public Works">Public Works</Option>
            <Option value="Health & Sanitation">Health & Sanitation</Option>
            <Option value="Transportation">Transportation</Option>
            <Option value="Revenue & Finance">Revenue & Finance</Option>
            <Option value="Education">Education</Option>
          </Select>
          <Select value={selectedStatus} onChange={setSelectedStatus} style={{ width: 140 }}>
            <Option value="All">All Statuses</Option>
            <Option value="Pending">Pending</Option>
            <Option value="In Progress">In Progress</Option>
            <Option value="Completed">Completed</Option>
          </Select>
          {user?.role !== 'staff' && (
            <Button 
              type="primary" 
              icon={<PlusOutlined />}
              onClick={() => {
                setEditingTask(null);
                form.resetFields();
                setIsModalOpen(true);
              }}
            >
              Create Task
            </Button>
          )}
        </Space>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title="Total Assigned Deliverables"
              value={filteredTasks.length}
              valueStyle={{ color: '#1890ff', fontWeight: 600 }}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#e6f7ff' }}>
            <Statistic
              title="Active In-Progress"
              value={filteredTasks.filter(t => t.status === 'In Progress').length}
              valueStyle={{ color: '#096dd9', fontWeight: 600 }}
              prefix={<ClockCircleOutlined style={{ color: '#096dd9' }} />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title="Resolved / Completed"
              value={filteredTasks.filter(t => t.status === 'Completed').length}
              valueStyle={{ color: '#52c41a', fontWeight: 600 }}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff1f0' }}>
            <Statistic
              title="Critical & High Urgency"
              value={filteredTasks.filter(t => t.priority === 'Critical' || t.priority === 'High').length}
              valueStyle={{ color: '#cf1322', fontWeight: 600 }}
              prefix={<AlertOutlined style={{ color: '#cf1322' }} />}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={filteredTasks}
          loading={loading}
          rowKey={r => r.task_id || r.id}
          pagination={{ pageSize: 8 }}
          size="middle"
        />
      </Card>

      <Modal
        title={editingTask ? `Edit Task ${editingTask.task_id}` : 'Create New Administrative Task'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingTask(null);
        }}
        footer={null}
        width={600}
      >
        <Form form={form} layout="vertical" onFinish={handleCreateOrUpdateTask}>
          <Form.Item name="task_name" label="Task Title / Deliverable" rules={[{ required: true, message: 'Please input task title' }]}>
            <Input placeholder="e.g. Inspect storm drain outflow at Ward 3" />
          </Form.Item>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="department" label="Responsible Department" initialValue="Public Works" rules={[{ required: true }]}>
                <Select>
                  <Option value="Public Works">Public Works</Option>
                  <Option value="Health & Sanitation">Health & Sanitation</Option>
                  <Option value="Transportation">Transportation</Option>
                  <Option value="Revenue & Finance">Revenue & Finance</Option>
                  <Option value="Education">Education</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="priority" label="Priority Level" initialValue="Medium">
                <Select>
                  <Option value="Low">Low</Option>
                  <Option value="Medium">Medium</Option>
                  <Option value="High">High</Option>
                  <Option value="Critical">Critical</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="assigned_to" label="Assignee (Officer Handle)" initialValue="staff">
                <Input placeholder="e.g. staff" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="due_date" label="Due Date">
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item name="description" label="Detailed Work Description">
            <TextArea rows={3} placeholder="Provide instructions, location coordinates, or requirements..." />
          </Form.Item>
          <div style={{ textAlign: 'right', marginTop: 16 }}>
            <Space>
              <Button onClick={() => {
                setIsModalOpen(false);
                setEditingTask(null);
              }}>Cancel</Button>
              <Button type="primary" htmlType="submit">
                {editingTask ? 'Save Changes' : 'Dispatch Task'}
              </Button>
            </Space>
          </div>
        </Form>
      </Modal>
    </div>
  );
};

export default TaskTracking;
