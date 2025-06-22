import React, { useState, useEffect } from 'react';
import { Card, Button, Table, Tag, Space, Alert } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';

const TaskTracking = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);

  // Mock task data for demonstration
  const mockTasks = [
    {
      id: '1',
      task_id: 'T-001',
      task_name: 'Road Maintenance Survey',
      description: 'Conduct comprehensive survey of main roads',
      priority: 'High',
      status: 'In Progress',
      assigned_to: 'john_doe',
      due_date: '2025-07-15',
      department: 'Public Works',
    },
    {
      id: '2',
      task_id: 'T-002',
      task_name: 'Budget Report Preparation',
      description: 'Prepare quarterly budget analysis report',
      priority: 'Medium',
      status: 'Pending',
      assigned_to: 'jane_smith',
      due_date: '2025-07-20',
      department: 'Finance',
    },
    {
      id: '3',
      task_id: 'T-003',
      task_name: 'Health Inspection',
      description: 'Monthly health facility inspection',
      priority: 'Critical',
      status: 'Completed',
      assigned_to: 'mike_johnson',
      due_date: '2025-06-30',
      department: 'Health',
    },
  ];

  useEffect(() => {
    // Filter tasks based on user role
    let filteredTasks = mockTasks;
    if (user?.role === 'staff') {
      filteredTasks = mockTasks.filter(task => task.assigned_to === user.username);
    } else if (user?.role === 'department_head') {
      filteredTasks = mockTasks.filter(task => task.department === user.department);
    }
    setTasks(filteredTasks);
  }, [user]);

  const getStatusColor = (status) => {
    const colors = {
      'Pending': 'orange',
      'In Progress': 'blue',
      'Completed': 'green',
      'Canceled': 'red',
    };
    return colors[status] || 'default';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      'Low': 'green',
      'Medium': 'orange',
      'High': 'red',
      'Critical': 'purple',
    };
    return colors[priority] || 'default';
  };

  const columns = [
    {
      title: 'Task ID',
      dataIndex: 'task_id',
      key: 'task_id',
    },
    {
      title: 'Task Name',
      dataIndex: 'task_name',
      key: 'task_name',
    },
    {
      title: 'Assigned To',
      dataIndex: 'assigned_to',
      key: 'assigned_to',
    },
    {
      title: 'Priority',
      dataIndex: 'priority',
      key: 'priority',
      render: (priority) => (
        <Tag color={getPriorityColor(priority)}>{priority}</Tag>
      ),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>{status}</Tag>
      ),
    },
    {
      title: 'Due Date',
      dataIndex: 'due_date',
      key: 'due_date',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            type="text"
            icon={<EditOutlined />}
            onClick={() => console.log('Edit task:', record.id)}
          />
          {user?.role !== 'staff' && (
            <Button
              type="text"
              danger
              icon={<DeleteOutlined />}
              onClick={() => console.log('Delete task:', record.id)}
            />
          )}
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <h1>Task Tracking</h1>
        {user?.role !== 'staff' && (
          <Button type="primary" icon={<PlusOutlined />}>
            Create Task
          </Button>
        )}
      </div>

      <Alert
        message="Demo Mode"
        description="Task management functionality is shown with sample data. In production, this would connect to the backend API."
        type="info"
        showIcon
        style={{ marginBottom: 16 }}
      />

      <Card>
        <Table
          columns={columns}
          dataSource={tasks}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
};

export default TaskTracking;