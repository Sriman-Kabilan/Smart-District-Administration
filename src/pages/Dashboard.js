import React, { useState } from 'react';
import { 
  Row, Col, Card, Statistic, Select, Table, Tag, Progress, 
  Button, Space, message, Badge, Timeline 
} from 'antd';
import { 
  ArrowUpOutlined, CheckCircleOutlined, ClockCircleOutlined, 
  TeamOutlined, BankOutlined, AlertOutlined, RiseOutlined 
} from '@ant-design/icons';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { useAuth } from '../contexts/AuthContext';

const { Option } = Select;

// Admin Chart Datasets
const departmentPerformanceData = [
  { department: 'Public Works', resolved: 42, pending: 12 },
  { department: 'Health', resolved: 38, pending: 8 },
  { department: 'Education', resolved: 25, pending: 5 },
  { department: 'Finance', resolved: 19, pending: 4 },
  { department: 'Transport', resolved: 28, pending: 10 },
  { department: 'Environment', resolved: 16, pending: 3 }
];

const budgetShareData = [
  { name: 'Public Works', value: 36, color: '#1890ff' },
  { name: 'Health & Sanitation', value: 26, color: '#52c41a' },
  { name: 'Transportation', value: 17, color: '#faad14' },
  { name: 'Education', value: 12, color: '#722ed1' },
  { name: 'IT & Finance', value: 9, color: '#13c2c2' }
];

const departmentHeadTeam = [
  { key: '1', name: 'Robert Martinez', role: 'Senior Field Engineer', activeTasks: 4, efficiency: 94 },
  { key: '2', name: 'Sarah Jenkins', role: 'Water Quality Inspector', activeTasks: 3, efficiency: 96 },
  { key: '3', name: 'David Chen', role: 'Civil Maintenance Officer', activeTasks: 5, efficiency: 88 },
  { key: '4', name: 'Elena Rostova', role: 'Permit & Compliance Officer', activeTasks: 2, efficiency: 92 }
];

const staffTasksList = [
  { key: '1', id: 'T-101', title: 'Survey Main Canal Drainage Choke Point', priority: 'Critical', due: 'Today', status: 'In Progress' },
  { key: '2', id: 'T-104', title: 'Compile Weekly Asphalt Inspection Log', priority: 'High', due: 'Tomorrow', status: 'Pending' },
  { key: '3', id: 'T-108', title: 'Verify Chlorine Sensor Telemetry at Ward 4', priority: 'Medium', due: 'Nov 14', status: 'Completed' },
  { key: '4', id: 'T-112', title: 'Submit Fuel Consumption Log for Fleet #3', priority: 'Normal', due: 'Nov 16', status: 'Pending' }
];

const recentActivities = [
  { color: 'green', text: 'Health & Sanitation resolved 14 water testing grievances in Ward 2' },
  { color: 'blue', text: 'Public Works dispatched asphalt crew to Flyover Junction 4' },
  { color: 'orange', text: 'Transportation issued route adjustment circular for Bus Corridor 8' },
  { color: 'purple', text: 'Treasury approved $450K Q3 infrastructure allocation' }
];

const Dashboard = () => {
  const { user } = useAuth();
  const [selectedDepartment, setSelectedDepartment] = useState('All');
  const [myTasks, setMyTasks] = useState(staffTasksList);

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
      my_tasks: myTasks.filter(t => t.status !== 'Completed').length,
      completed_week: 5,
      pending_tasks: myTasks.filter(t => t.status === 'Pending').length,
    }
  };

  const data = mockData[user?.role] || mockData.administrator;

  const toggleTaskStatus = (key) => {
    setMyTasks(myTasks.map(t => {
      if (t.key === key) {
        const nextStatus = t.status === 'Completed' ? 'In Progress' : 'Completed';
        message.success(`Task ${t.id} marked as ${nextStatus}`);
        return { ...t, status: nextStatus };
      }
      return t;
    }));
  };

  const renderAdminDashboard = () => (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title="Total Departments"
              value={data.total_departments}
              prefix={<BankOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>7 active administrative units</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title="Active District Tasks"
              value={data.active_tasks}
              valueStyle={{ color: '#52c41a', fontWeight: 600 }}
              prefix={<RiseOutlined style={{ color: '#52c41a' }} />}
              suffix={`+${data.task_change_percent}%`}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>18 resolved in last 24 hrs</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f9f0ff' }}>
            <Statistic
              title="Total District Workforce"
              value={data.total_staff}
              prefix={<TeamOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#722ed1', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#722ed1' }}>94% on-duty readiness</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title="Fiscal Budget Utilization"
              value={data.budget_utilization}
              precision={1}
              suffix="%"
              prefix={<CheckCircleOutlined style={{ color: '#fa8c16' }} />}
              valueStyle={{ color: '#fa8c16', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#fa8c16' }}>Within target fiscal burn envelope</div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={15}>
          <Card title="Departmental Workload & Case Resolution Throughput">
            <div style={{ height: 320 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={departmentPerformanceData}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="department" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="resolved" name="Resolved Tasks" fill="#52c41a" />
                  <Bar dataKey="pending" name="In-Queue / Pending" fill="#1890ff" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={9}>
          <Card title="District Budget Allocation Share">
            <div style={{ height: 320 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={budgetShareData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
                    {budgetShareData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={v => `${v}% of Total Budget`} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card title="Live District Operational Timeline">
            <Timeline items={recentActivities} />
          </Card>
        </Col>
      </Row>
    </div>
  );

  const renderDepartmentHeadDashboard = () => (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title="Department Tasks"
              value={data.department_tasks}
              valueStyle={{ color: '#1890ff', fontWeight: 600 }}
              prefix={<ArrowUpOutlined />}
              suffix={`+${data.task_change_percent}%`}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title="Team Completion Rate"
              value={data.completion_rate}
              precision={1}
              suffix="%"
              valueStyle={{ color: '#52c41a', fontWeight: 600 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f9f0ff' }}>
            <Statistic
              title="Assigned Personnel"
              value={data.team_members}
              valueStyle={{ color: '#722ed1', fontWeight: 600 }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title="Department Efficiency"
              value={data.efficiency_score}
              precision={1}
              valueStyle={{ color: '#fa8c16', fontWeight: 600 }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={14}>
          <Card title="Team Member Workload & Performance">
            <Table
              dataSource={departmentHeadTeam}
              columns={[
                { title: 'Officer Name', dataIndex: 'name', key: 'name', render: t => <strong>{t}</strong> },
                { title: 'Role Designation', dataIndex: 'role', key: 'role' },
                { title: 'Active Assignments', dataIndex: 'activeTasks', key: 'activeTasks', render: a => <Badge count={a} style={{ backgroundColor: '#1890ff' }} /> },
                { 
                  title: 'Efficiency Rating', 
                  dataIndex: 'efficiency', 
                  key: 'efficiency', 
                  render: e => <Progress percent={e} size="small" status="active" /> 
                }
              ]}
              pagination={false}
              size="middle"
            />
          </Card>
        </Col>
        <Col xs={24} lg={10}>
          <Card title="Department Priority Directives">
            <div style={{ padding: '8px 0' }}>
              <div style={{ padding: 12, background: '#fff1f0', borderRadius: 6, marginBottom: 12 }}>
                <strong style={{ color: '#cf1322' }}>🚨 Immediate Escalation:</strong>
                <div>Expedite culvert clearance in Ward 2 before monsoon surge.</div>
              </div>
              <div style={{ padding: 12, background: '#f6ffed', borderRadius: 6, marginBottom: 12 }}>
                <strong style={{ color: '#389e0d' }}>✅ Milestone Achieved:</strong>
                <div>Quarterly road safety inspection completed with zero overdue items.</div>
              </div>
              <div style={{ padding: 12, background: '#e6f7ff', borderRadius: 6 }}>
                <strong style={{ color: '#096dd9' }}>ℹ️ Upcoming Audit:</strong>
                <div>State municipal audit scheduled for Nov 22. All logs pre-indexed.</div>
              </div>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );

  const renderStaffDashboard = () => (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={8}>
          <Card bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title="My Assigned Tasks"
              value={data.my_tasks}
              valueStyle={{ color: '#1890ff', fontWeight: 600 }}
              prefix={<ClockCircleOutlined />}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>Currently in work queue</div>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title="Resolved This Week"
              value={data.completed_week}
              valueStyle={{ color: '#52c41a', fontWeight: 600 }}
              prefix={<CheckCircleOutlined />}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>+2 ahead of quota</div>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title="Pending Execution"
              value={data.pending_tasks}
              valueStyle={{ color: '#fa8c16', fontWeight: 600 }}
              prefix={<AlertOutlined />}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#fa8c16' }}>Scheduled for review</div>
          </Card>
        </Col>
      </Row>

      <Card title="My Active Assignments & Field Tasks">
        <Table
          dataSource={myTasks}
          columns={[
            { title: 'Task ID', dataIndex: 'id', key: 'id', render: id => <Tag color="blue">{id}</Tag> },
            { title: 'Deliverable Title', dataIndex: 'title', key: 'title', render: t => <strong>{t}</strong> },
            { 
              title: 'Priority', 
              dataIndex: 'priority', 
              key: 'priority',
              render: p => <Tag color={p === 'Critical' ? 'red' : p === 'High' ? 'orange' : 'blue'}>{p}</Tag>
            },
            { title: 'Due Date', dataIndex: 'due', key: 'due' },
            { 
              title: 'Status', 
              dataIndex: 'status', 
              key: 'status',
              render: s => <Tag color={s === 'Completed' ? 'green' : s === 'In Progress' ? 'blue' : 'orange'}>{s}</Tag>
            },
            {
              title: 'Action',
              key: 'action',
              render: (_, record) => (
                <Button 
                  size="small" 
                  type={record.status === 'Completed' ? 'default' : 'primary'}
                  onClick={() => toggleTaskStatus(record.key)}
                >
                  {record.status === 'Completed' ? 'Re-open' : 'Mark Done'}
                </Button>
              )
            }
          ]}
          pagination={false}
          size="middle"
        />
      </Card>
    </div>
  );

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>
            {user?.role === 'administrator' && 'District Executive Command Dashboard'}
            {user?.role === 'department_head' && `${user.department || 'Department'} Operations Dashboard`}
            {user?.role === 'staff' && 'My Field Work & Task Portal'}
          </h1>
          <span style={{ color: '#8c8c8c' }}>
            Logged in as <strong>{user?.full_name || 'Officer'}</strong> ({user?.role?.replace('_', ' ').toUpperCase()})
          </span>
        </div>
        {user?.role === 'administrator' && (
          <Select value={selectedDepartment} onChange={setSelectedDepartment} style={{ width: 200 }}>
            <Option value="All">All District Units</Option>
            <Option value="Public Works">Public Works</Option>
            <Option value="Health">Health & Sanitation</Option>
            <Option value="Transport">Transportation</Option>
          </Select>
        )}
      </div>

      {user?.role === 'administrator' && renderAdminDashboard()}
      {user?.role === 'department_head' && renderDepartmentHeadDashboard()}
      {user?.role === 'staff' && renderStaffDashboard()}
    </div>
  );
};

export default Dashboard;
