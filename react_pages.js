// pages/Dashboard.js - Main Dashboard Component
import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Tabs, Spin, Select } from 'antd';
import { useAuth } from '../contexts/AuthContext';
import { dashboardService } from '../services/dashboard';
import { KPICard } from '../components/Common/KPICard';
import PerformanceChart from '../components/Charts/PerformanceChart';
import ResourceChart from '../components/Charts/ResourceChart';
import TaskList from '../components/Tasks/TaskList';

const { TabPane } = Tabs;
const { Option } = Select;

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);
  const [selectedDepartment, setSelectedDepartment] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, [selectedDepartment]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await dashboardService.getOverviewData(selectedDepartment);
      setDashboardData(data);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    );
  }

  const renderAdminDashboard = () => (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <KPICard
            title="Total Departments"
            value={dashboardData?.total_departments || 0}
            color="#1890ff"
          />
        </Col>
        <Col span={6}>
          <KPICard
            title="Active Tasks"
            value={dashboardData?.active_tasks || 0}
            delta={dashboardData?.task_change_percent}
            color="#52c41a"
          />
        </Col>
        <Col span={6}>
          <KPICard
            title="Total Staff"
            value={dashboardData?.total_staff || 0}
            color="#722ed1"
          />
        </Col>
        <Col span={6}>
          <KPICard
            title="Budget Utilization"
            value={dashboardData?.budget_utilization || 0}
            precision={1}
            suffix="%"
            color="#fa8c16"
          />
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="Performance Trends">
            <PerformanceChart data={dashboardData?.performance_data} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Resource Allocation">
            <ResourceChart data={dashboardData?.resource_data} />
          </Card>
        </Col>
      </Row>
    </div>
  );

  const renderDepartmentHeadDashboard = () => (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <KPICard
            title="Department Tasks"
            value={dashboardData?.department_tasks || 0}
            delta={dashboardData?.task_change_percent}
            color="#1890ff"
          />
        </Col>
        <Col span={6}>
          <KPICard
            title="Completion Rate"
            value={dashboardData?.completion_rate || 0}
            precision={1}
            suffix="%"
            color="#52c41a"
          />
        </Col>
        <Col span={6}>
          <KPICard
            title="Team Members"
            value={dashboardData?.team_members || 0}
            color="#722ed1"
          />
        </Col>
        <Col span={6}>
          <KPICard
            title="Efficiency Score"
            value={dashboardData?.efficiency_score || 0}
            precision={2}
            color="#fa8c16"
          />
        </Col>
      </Row>

      <Tabs defaultActiveKey="overview">
        <TabPane tab="Overview" key="overview">
          <Row gutter={16}>
            <Col span={12}>
              <Card title="Task Distribution">
                <PerformanceChart data={dashboardData?.task_distribution} />
              </Card>
            </Col>
            <Col span={12}>
              <Card title="Team Performance">
                <ResourceChart data={dashboardData?.team_performance} />
              </Card>
            </Col>
          </Row>
        </TabPane>
        <TabPane tab="Recent Tasks" key="tasks">
          <TaskList filters={{ department: user.department, limit: 10 }} />
        </TabPane>
      </Tabs>
    </div>
  );

  const renderStaffDashboard = () => (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <KPICard
            title="My Tasks"
            value={dashboardData?.my_tasks || 0}
            color="#1890ff"
          />
        </Col>
        <Col span={8}>
          <KPICard
            title="Completed This Week"
            value={dashboardData?.completed_week || 0}
            color="#52c41a"
          />
        </Col>
        <Col span={8}>
          <KPICard
            title="Pending Tasks"
            value={dashboardData?.pending_tasks || 0}
            color="#fa541c"
          />
        </Col>
      </Row>

      <Card title="My Recent Tasks">
        <TaskList filters={{ assigned_to: user.username, limit: 10 }} />
      </Card>
    </div>
  );

  return (
    <div>
      <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
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

      {user?.role === 'administrator' && renderAdminDashboard()}
      {user?.role === 'department_head' && renderDepartmentHeadDashboard()}
      {user?.role === 'staff' && renderStaffDashboard()}
    </div>
  );
};

// pages/TaskTracking.js - Task Management Page
import React, { useState, useEffect } from 'react';
import { Card, Button, Modal, Form, Input, Select, DatePicker, Table, Tag, Space, message } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { taskService } from '../services/tasks';
import { authService } from '../services/auth';
import { useAuth } from '../contexts/AuthContext';
import moment from 'moment';

const { Option } = Select;
const { TextArea } = Input;

const TaskTracking = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [users, setUsers] = useState([]);
  const [form] = Form.useForm();

  useEffect(() => {
    loadTasks();
    if (user?.role !== 'staff') {
      loadUsers();
    }
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const filters = user?.role === 'staff' ? { assigned_to: user.username } : {};
      if (user?.role === 'department_head') {
        filters.department = user.department;
      }
      const tasksData = await taskService.getTasks(filters);
      setTasks(tasksData);
    } catch (error) {
      message.error('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const loadUsers = async () => {
    try {
      const usersData = await authService.getAllUsers();
      setUsers(usersData);
    } catch (error) {
      console.error('Failed to load users');
    }
  };

  const handleCreateTask = () => {
    setEditingTask(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    form.setFieldsValue({
      ...task,
      due_date: moment(task.due_date),
    });
    setModalVisible(true);
  };

  const handleSubmit = async (values) => {
    try {
      const taskData = {
        ...values,
        due_date: values.due_date.format('YYYY-MM-DD'),
        created_by: user.username,
        department: user.department,
      };

      if (editingTask) {
        await taskService.updateTask(editingTask.id, taskData);
        message.success('Task updated successfully');
      } else {
        await taskService.createTask(taskData);
        message.success('Task created successfully');
      }

      setModalVisible(false);
      loadTasks();
    } catch (error) {
      message.error('Failed to save task');
    }
  };

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await taskService.updateTaskStatus(taskId, newStatus);
      message.success('Task status updated');
      loadTasks();
    } catch (error) {
      message.error('Failed to update task status');
    }
  };

  const handleDelete = async (taskId) => {
    try {
      await taskService.deleteTask(taskId);
      message.success('Task deleted successfully');
      loadTasks();
    } catch (error) {
      message.error('Failed to delete task');
    }
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
      render: (status, record) => (
        <Select
          value={status}
          style={{ width: 120 }}
          onChange={(newStatus) => handleStatusChange(record.id, newStatus)}
          disabled={user?.role === 'staff' && record.assigned_to !== user.username}
        >
          <Option value="Pending">Pending</Option>
          <Option value="In Progress">In Progress</Option>
          <Option value="Completed">Completed</Option>
          <Option value="Canceled">Canceled</Option>
        </Select>
      ),
    },
    {
      title: 'Due Date',
      dataIndex: 'due_date',
      key: 'due_date',
      render: (date) => moment(date).format('MMM DD, YYYY'),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          {(user?.role !== 'staff' || record.assigned_to === user.username) && (
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => handleEditTask(record)}
            />
          )}
          {user?.role !== 'staff' && (
            <Button
              type="text"
              danger
              icon={<DeleteOutlined />}
              onClick={() => handleDelete(record.id)}
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
          <Button type="primary" icon={<PlusOutlined />} onClick={handleCreateTask}>
            Create Task
          </Button>
        )}
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={tasks}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={editingTask ? 'Edit Task' : 'Create Task'}
        visible={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        width={600}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item
            name="task_name"
            label="Task Name"
            rules={[{ required: true, message: 'Please enter task name' }]}
          >
            <Input placeholder="Enter task name" />
          </Form.Item>

          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter description' }]}
          >
            <TextArea rows={4} placeholder="Enter task description" />
          </Form.Item>

          <Form.Item
            name="assigned_to"
            label="Assign To"
            rules={[{ required: true, message: 'Please select assignee' }]}
          >
            <Select placeholder="Select assignee">
              {users
                .filter(u => u.role === 'staff' && u.department === user.department)
                .map(u => (
                  <Option key={u.id} value={u.username}>
                    {u.full_name} ({u.username})
                  </Option>
                ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="priority"
            label="Priority"
            rules={[{ required: true, message: 'Please select priority' }]}
          >
            <Select placeholder="Select priority">
              <Option value="Low">Low</Option>
              <Option value="Medium">Medium</Option>
              <Option value="High">High</Option>
              <Option value="Critical">Critical</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="due_date"
            label="Due Date"
            rules={[{ required: true, message: 'Please select due date' }]}
          >
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit">
                {editingTask ? 'Update' : 'Create'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

// pages/PredictiveAnalytics.js - AI Analytics Page
import React, { useState, useEffect } from 'react';
import { Card, Tabs, Select, Button, Slider, Row, Col, Statistic, Spin, message } from 'antd';
import { analyticsService } from '../services/analytics';
import { useAuth } from '../contexts/AuthContext';
import PredictiveChart from '../components/Charts/PredictiveChart';

const { TabPane } = Tabs;
const { Option } = Select;

const PredictiveAnalytics = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState(null);
  const [optimization, setOptimization] = useState(null);
  const [selectedDepartment, setSelectedDepartment] = useState(user?.department || 'Public Works');
  const [predictionPeriods, setPredictionPeriods] = useState(3);
  const [modelType, setModelType] = useState('random_forest');
  
  // Scenario analysis state
  const [budgetChange, setBudgetChange] = useState(0);
  const [staffChange, setStaffChange] = useState(0);
  const [equipmentChange, setEquipmentChange] = useState(0);
  const [scenarioResults, setScenarioResults] = useState(null);

  useEffect(() => {
    if (user?.role !== 'staff') {
      loadPredictions();
      loadOptimization();
    }
  }, [selectedDepartment, predictionPeriods, modelType]);

  const loadPredictions = async () => {
    try {
      setLoading(true);
      const data = await analyticsService.getPredictions(
        selectedDepartment,
        predictionPeriods,
        modelType
      );
      setPredictions(data);
    } catch (error) {
      message.error('Failed to load predictions');
    } finally {
      setLoading(false);
    }
  };

  const loadOptimization = async () => {
    try {
      const data = await analyticsService.getOptimalAllocation(selectedDepartment);
      setOptimization(data);
    } catch (error) {
      console.error('Failed to load optimization data');
    }
  };

  const runScenarioAnalysis = async () => {
    try {
      setLoading(true);
      const scenarios = {
        budget_change: budgetChange,
        staff_change: staffChange,
        equipment_change: equipmentChange,
      };
      const results = await analyticsService.runScenarioAnalysis(selectedDepartment, scenarios);
      setScenarioResults(results);
    } catch (error) {
      message.error('Failed to run scenario analysis');
    } finally {
      setLoading(false);
    }
  };

  if (user?.role === 'staff') {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <h2>Access Restricted</h2>
        <p>You don't have permission to access AI predictive analytics.</p>
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>AI-Driven Predictive Analytics</h1>
        {user?.role === 'administrator' && (
          <Select
            value={selectedDepartment}
            style={{ width: 200 }}
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

      <Tabs defaultActiveKey="predictions">
        <TabPane tab="Resource Prediction" key="predictions">
          <Card title="Prediction Settings" style={{ marginBottom: 16 }}>
            <Row gutter={16}>
              <Col span={8}>
                <label>Prediction Periods (Months)</label>
                <Slider
                  min={1}
                  max={12}
                  value={predictionPeriods}
                  onChange={setPredictionPeriods}
                  marks={{ 1: '1', 6: '6', 12: '12' }}
                />
              </Col>
              <Col span={8}>
                <label>Model Type</label>
                <Select
                  value={modelType}
                  style={{ width: '100%' }}
                  onChange={setModelType}
                >
                  <Option value="random_forest">Random Forest</Option>
                  <Option value="linear">Linear Regression</Option>
                  <Option value="arima">ARIMA</Option>
                </Select>
              </Col>
              <Col span={8}>
                <Button type="primary" onClick={loadPredictions} loading={loading}>
                  Generate Predictions
                </Button>
              </Col>
            </Row>
          </Card>

          {loading ? (
            <div style={{ textAlign: 'center', padding: '50px' }}>
              <Spin size="large" />
            </div>
          ) : (
            predictions && (
              <Card title="Prediction Results">
                <PredictiveChart data={predictions} />
              </Card>
            )
          )}
        </TabPane>

        <TabPane tab="Optimization Analysis" key="optimization">
          {optimization && (
            <div>
              <Row gutter={16} style={{ marginBottom: 24 }}>
                <Col span={8}>
                  <Card title="Budget Allocation">
                    <Statistic
                      title="Current"
                      value={optimization.current.budget}
                      precision={2}
                      prefix="$"
                    />
                    <Statistic
                      title="Recommended"
                      value={optimization.recommended.budget}
                      precision={2}
                      prefix="$"
                      valueStyle={{
                        color: optimization.change.budget > 0 ? '#cf1322' : '#3f8600'
                      }}
                    />
                  </Card>
                </Col>
                <Col span={8}>
                  <Card title="Staff Allocation">
                    <Statistic
                      title="Current"
                      value={optimization.current.staff}
                    />
                    <Statistic
                      title="Recommended"
                      value={optimization.recommended.staff}
                      valueStyle={{
                        color: optimization.change.staff > 0 ? '#cf1322' : '#3f8600'
                      }}
                    />
                  </Card>
                </Col>
                <Col span={8}>
                  <Card title="Equipment Allocation">
                    <Statistic
                      title="Current"
                      value={optimization.current.equipment}
                      precision={2}
                      prefix="$"
                    />
                    <Statistic
                      title="Recommended"
                      value={optimization.recommended.equipment}
                      precision={2}
                      prefix="$"
                      valueStyle={{
                        color: optimization.change.equipment > 0 ? '#cf1322' : '#3f8600'
                      }}
                    />
                  </Card>
                </Col>
              </Row>

              <Card title="AI Analysis">
                <p>{optimization.explanation}</p>
              </Card>
            </div>
          )}
        </TabPane>

        <TabPane tab="What-If Scenarios" key="scenarios">
          <Card title="Scenario Configuration" style={{ marginBottom: 16 }}>
            <Row gutter={16}>
              <Col span={8}>
                <label>Budget Change (%)</label>
                <Slider
                  min={-30}
                  max={50}
                  value={budgetChange}
                  onChange={setBudgetChange}
                  marks={{ '-30': '-30%', 0: '0%', 50: '50%' }}
                />
              </Col>
              <Col span={8}>
                <label>Staff Change</label>
                <Slider
                  min={-10}
                  max={20}
                  value={staffChange}
                  onChange={setStaffChange}
                  marks={{ '-10': '-10', 0: '0', 20: '+20' }}
                />
              </Col>
              <Col span={8}>
                <label>Equipment Change (%)</label>
                <Slider
                  min={-30}
                  max={50}
                  value={equipmentChange}
                  onChange={setEquipmentChange}
                  marks={{ '-30': '-30%', 0: '0%', 50: '50%' }}
                />
              </Col>
            </Row>
            <div style={{ textAlign: 'center', marginTop: 16 }}>
              <Button type="primary" onClick={runScenarioAnalysis} loading={loading}>
                Run Scenario Analysis
              </Button>
            </div>
          </Card>

          {scenarioResults && (
            <Card title="Scenario Results">
              <Row gutter={16}>
                <Col span={8}>
                  <Statistic
                    title="Efficiency Score Impact"
                    value={scenarioResults.efficiency_change}
                    precision={2}
                    suffix="%"
                    valueStyle={{
                      color: scenarioResults.efficiency_change > 0 ? '#3f8600' : '#cf1322'
                    }}
                  />
                </Col>
                <Col span={8}>
                  <Statistic
                    title="Task Completion Impact"
                    value={scenarioResults.completion_change}
                    precision={2}
                    suffix="%"
                    valueStyle={{
                      color: scenarioResults.completion_change > 0 ? '#3f8600' : '#cf1322'
                    }}
                  />
                </Col>
                <Col span={8}>
                  <Statistic
                    title="Satisfaction Impact"
                    value={scenarioResults.satisfaction_change}
                    precision={2}
                    suffix="%"
                    valueStyle={{
                      color: scenarioResults.satisfaction_change > 0 ? '#3f8600' : '#cf1322'
                    }}
                  />
                </Col>
              </Row>
              <div style={{ marginTop: 16 }}>
                <h4>Analysis Insights:</h4>
                <ul>
                  {scenarioResults.insights.map((insight, index) => (
                    <li key={index}>{insight}</li>
                  ))}
                </ul>
              </div>
            </Card>
          )}
        </TabPane>
      </Tabs>
    </div>
  );
};

export { Dashboard, TaskTracking, PredictiveAnalytics };