import React, { useState, useEffect } from 'react';
import { 
  Card, Button, Table, Tag, Space, Alert, Modal, Form, 
  Input, Select, DatePicker, Row, Col, Statistic, Popconfirm, 
  message, Dropdown, Drawer, Descriptions, Divider 
} from 'antd';
import { 
  PlusOutlined, EditOutlined, DeleteOutlined, CheckCircleOutlined, 
  ClockCircleOutlined, AlertOutlined, DownOutlined, FilterOutlined,
  FileTextOutlined, EyeOutlined, UserOutlined, BankOutlined 
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
    description: 'Conduct comprehensive survey of arterial roads in Ward 2. Document surface degradation, measure asphalt depth loss, and tag GPS coordinates of high-risk potholes ahead of monsoon rain forecast.',
    priority: 'High',
    status: 'In Progress',
    assigned_to: 'staff',
    due_date: '2026-11-20',
    department: 'Public Works',
    location: 'Ward 2 - Riverside Basin Road (KM 4 - 12)',
    notes: 'Coordinate with traffic police for partial lane closure during 10:00 PM to 04:00 AM survey window.'
  },
  {
    id: '2',
    task_id: 'T-002',
    task_name: 'Quarterly Municipal Budget Reconciliation',
    description: 'Prepare expenditure reconciliation for Q3 audit. Audit heavy fleet diesel consumption vouchers, overtime payroll authorizations, and capital equipment procurement ledgers.',
    priority: 'Medium',
    status: 'Pending',
    assigned_to: 'dept_head',
    due_date: '2026-11-25',
    department: 'Revenue & Finance',
    location: 'District Civic Center, Finance Wing',
    notes: 'Draft preliminary statement before the standing treasury audit on Nov 22.'
  },
  {
    id: '3',
    task_id: 'T-003',
    task_name: 'Primary School Drinking Water Testing',
    description: 'Sample testing across 12 civic schools. Perform microbial culture and residual chlorine titration. Replace cartridge filters in schools failing potable water standards.',
    priority: 'Critical',
    status: 'Completed',
    assigned_to: 'staff',
    due_date: '2026-11-10',
    department: 'Health & Sanitation',
    location: 'Wards 1, 3, and 5 Public Primary Schools',
    notes: 'All 12 school water plants cleared WHO safety guidelines. Report filed with Education Officer.'
  },
  {
    id: '4',
    task_id: 'T-004',
    task_name: 'Traffic Signal Sensor Synchronization',
    description: 'Deploy firmware update to automated signal controllers along Ring Road Corridor to implement intelligent green-wave timing for morning peak transit buses.',
    priority: 'High',
    status: 'In Progress',
    assigned_to: 'staff',
    due_date: '2026-11-18',
    department: 'Transportation',
    location: 'Ring Road Junctions 3, 5, and 8',
    notes: 'Requires coordination with IT network team for fiber optic gateway handshake.'
  },
  {
    id: '5',
    task_id: 'T-005',
    task_name: 'Solar Panel Maintenance at Civic Center Block B',
    description: 'Routine inverter diagnostic, high-pressure dust cleaning, and battery telemetry calibration on 150kW rooftop photovoltaic array.',
    priority: 'Low',
    status: 'Pending',
    assigned_to: 'staff',
    due_date: '2026-11-30',
    department: 'Public Works',
    location: 'District Civic Center Rooftop',
    notes: 'Safety harnesses and roof anchor line inspection required before crew ascent.'
  }
];

const TaskTracking = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState(initialDistrictTasks);
  const [loading, setLoading] = useState(false);
  const [selectedDept, setSelectedDept] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');
  
  // Modals & Drawer State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [detailDrawerTask, setDetailDrawerTask] = useState(null);
  const [form] = Form.useForm();

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const res = await api.get('/tasks');
      if (res.data && Array.isArray(res.data) && res.data.length > 0) {
        setTasks(res.data);
      }
    } catch (err) {
      // Fallback to local state
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
        description: values.description,
        location: values.location,
        notes: values.notes
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
        location: values.location || 'District Jurisdiction',
        notes: values.notes || ''
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
    if (detailDrawerTask && (detailDrawerTask.task_id === taskId || detailDrawerTask.id === taskId)) {
      setDetailDrawerTask({ ...detailDrawerTask, status: newStatus });
    }
    try {
      await api.patch(`/tasks/${taskId}/status`, { status: newStatus });
    } catch (e) {
      // Local state already updated
    }
    message.success(`Task status updated to ${newStatus}`);
  };

  const handleDeleteTask = async (taskId) => {
    setTasks(tasks.filter(t => t.task_id !== taskId && t.id !== taskId));
    if (detailDrawerTask && (detailDrawerTask.task_id === taskId || detailDrawerTask.id === taskId)) {
      setDetailDrawerTask(null);
    }
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
      description: record.description,
      location: record.location,
      notes: record.notes
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
      width: 90,
      render: id => <Tag color="geekblue">{id}</Tag>
    },
    {
      title: 'Task Deliverable',
      dataIndex: 'task_name',
      key: 'task_name',
      render: (name, record) => (
        <div>
          <a 
            style={{ fontWeight: 600, color: '#1890ff', cursor: 'pointer' }}
            onClick={() => setDetailDrawerTask(record)}
          >
            {name}
          </a>
          <div style={{ fontSize: 12, color: '#8c8c8c', marginTop: 2 }}>
            <FileTextOutlined style={{ marginRight: 4 }} />
            {record.description ? `${record.description.substring(0, 65)}...` : 'Click to view description box'}
          </div>
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
      title: 'Assigned Officer',
      dataIndex: 'assigned_to',
      key: 'assigned_to',
      render: a => <Tag color="purple"><UserOutlined style={{ marginRight: 4 }} />{a}</Tag>
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
            icon={<EyeOutlined />}
            title="Inspect Description Box"
            onClick={() => setDetailDrawerTask(record)}
          />
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
          <span style={{ color: '#8c8c8c' }}>Assign, inspect description boxes, and resolve civic action deliverables</span>
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
          expandable={{
            expandedRowRender: record => (
              <div style={{ 
                background: '#fafafa', 
                padding: '16px 20px', 
                borderRadius: '6px', 
                borderLeft: '4px solid #1890ff' 
              }}>
                <div style={{ marginBottom: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
                  <FileTextOutlined style={{ color: '#1890ff' }} />
                  <strong>Task Scope & Full Description Box:</strong>
                </div>
                <p style={{ margin: 0, fontSize: 13, lineHeight: '1.6', color: '#262626' }}>
                  {record.description || 'No detailed description specified.'}
                </p>
                {record.location && (
                  <div style={{ marginTop: 8, fontSize: 12, color: '#595959' }}>
                    <strong>📍 Location Coordinates:</strong> {record.location}
                  </div>
                )}
                {record.notes && (
                  <div style={{ marginTop: 4, fontSize: 12, color: '#d48806' }}>
                    <strong>⚠️ Field Directive / Notes:</strong> {record.notes}
                  </div>
                )}
              </div>
            ),
            rowExpandable: record => !!record.description || !!record.notes
          }}
        />
      </Card>

      {/* Task Creation & Edit Modal */}
      <Modal
        title={editingTask ? `Edit Task ${editingTask.task_id}` : 'Create New Administrative Task'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingTask(null);
        }}
        footer={null}
        width={650}
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

          <Form.Item name="location" label="Location / Target Ward">
            <Input placeholder="e.g. Ward 2 Riverside Basin (KM 4 - 12)" />
          </Form.Item>

          {/* Dedicated Description Box Form Field */}
          <Form.Item 
            name="description" 
            label="Task Description Box (Detailed Scope & Directives)" 
            rules={[{ required: true, message: 'Please provide task description' }]}
          >
            <TextArea 
              rows={4} 
              showCount 
              maxLength={600}
              placeholder="Enter detailed work instructions, safety requirements, contractor specs, or equipment needed..." 
            />
          </Form.Item>

          <Form.Item name="notes" label="Special Field Notes & Contingencies">
            <Input placeholder="e.g. Requires safety line inspection or police traffic escort" />
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

      {/* Task Description & Detail Drawer */}
      <Drawer
        title={<span><FileTextOutlined style={{ color: '#1890ff', marginRight: 8 }} />Task Description Box & Telemetry</span>}
        placement="right"
        width={520}
        open={!!detailDrawerTask}
        onClose={() => setDetailDrawerTask(null)}
        extra={
          detailDrawerTask && (
            <Space>
              <Button 
                size="small" 
                type="primary"
                onClick={() => {
                  const t = detailDrawerTask;
                  setDetailDrawerTask(null);
                  openEditModal(t);
                }}
              >
                Edit
              </Button>
            </Space>
          )
        }
      >
        {detailDrawerTask && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <Tag color="geekblue" style={{ fontSize: 14, padding: '2px 8px' }}>{detailDrawerTask.task_id}</Tag>
              <Tag color={getPriorityColor(detailDrawerTask.priority)}>{detailDrawerTask.priority} Priority</Tag>
            </div>

            <h3 style={{ margin: '0 0 12px 0' }}>{detailDrawerTask.task_name}</h3>

            <Descriptions column={1} size="small" bordered style={{ marginBottom: 20 }}>
              <Descriptions.Item label="Department">
                <Tag color="blue">{detailDrawerTask.department}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Assignee">
                <Tag color="purple"><UserOutlined style={{ marginRight: 4 }} />{detailDrawerTask.assigned_to}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Status">
                <Tag color={getStatusColor(detailDrawerTask.status)}>{detailDrawerTask.status}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Due Date">
                {detailDrawerTask.due_date}
              </Descriptions.Item>
              {detailDrawerTask.location && (
                <Descriptions.Item label="Location">
                  {detailDrawerTask.location}
                </Descriptions.Item>
              )}
            </Descriptions>

            <Divider orientation="left">Detailed Description Box</Divider>
            <div style={{ 
              background: '#f9f9f9', 
              padding: '16px', 
              borderRadius: '8px', 
              border: '1px solid #e8e8e8',
              lineHeight: 1.6,
              fontSize: 14,
              whiteSpace: 'pre-wrap'
            }}>
              {detailDrawerTask.description || 'No detailed description available for this deliverable.'}
            </div>

            {detailDrawerTask.notes && (
              <>
                <Divider orientation="left">Field Notes & Warnings</Divider>
                <Alert
                  message={detailDrawerTask.notes}
                  type="warning"
                  showIcon
                />
              </>
            )}

            <div style={{ marginTop: 24, textAlign: 'center' }}>
              <Button 
                block 
                type={detailDrawerTask.status === 'Completed' ? 'default' : 'primary'}
                onClick={() => handleStatusChange(
                  detailDrawerTask.task_id || detailDrawerTask.id, 
                  detailDrawerTask.status === 'Completed' ? 'In Progress' : 'Completed'
                )}
              >
                {detailDrawerTask.status === 'Completed' ? 'Re-open Task' : 'Mark Task as Completed'}
              </Button>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  );
};

export default TaskTracking;
