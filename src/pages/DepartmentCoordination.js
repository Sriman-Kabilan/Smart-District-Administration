import React, { useState } from 'react';
import { 
  Card, Row, Col, Table, Button, Modal, Form, Input, Select, Tag, 
  Timeline, Tabs, Space, Badge, message, Avatar, Tooltip, Progress 
} from 'antd';
import { 
  MessageOutlined, TeamOutlined, SendOutlined, PlusOutlined, 
  CalendarOutlined, FileTextOutlined, CheckCircleOutlined, 
  ClockCircleOutlined, ExclamationCircleOutlined 
} from '@ant-design/icons';

const { Option } = Select;
const { TextArea } = Input;

// Collaborative Projects
const initialProjects = [
  {
    key: '1',
    name: 'Monsoon Flood Mitigation & Drainage Revamp',
    departments: ['Public Works', 'Urban Planning', 'Health & Sanitation'],
    status: 'In Progress',
    progress: 68,
    lead: 'Public Works',
    deadline: '2026-12-15',
    budget: '$1.4M'
  },
  {
    key: '2',
    name: 'District Smart Traffic & Bus Rapid Transit (BRT) Sync',
    departments: ['Transportation', 'IT & Digital Services', 'Public Works'],
    status: 'In Progress',
    progress: 45,
    lead: 'Transportation',
    deadline: '2027-02-28',
    budget: '$850K'
  },
  {
    key: '3',
    name: 'School Nutritional Hygiene & Water Testing Drive',
    departments: ['Education', 'Health & Sanitation'],
    status: 'Completed',
    progress: 100,
    lead: 'Health & Sanitation',
    deadline: '2026-11-05',
    budget: '$320K'
  },
  {
    key: '4',
    name: 'Municipal GIS Property Tax Mapping Initiative',
    departments: ['Revenue & Finance', 'IT & Digital Services', 'Urban Planning'],
    status: 'In Progress',
    progress: 82,
    lead: 'Revenue & Finance',
    deadline: '2026-11-30',
    budget: '$450K'
  }
];

// Meetings
const initialMeetings = [
  {
    key: '1',
    title: 'Weekly District Inter-Departmental Steering Meeting',
    datetime: 'Nov 12, 2026 at 10:00 AM',
    location: 'District Magistrate Conference Hall A',
    leadDept: 'Administration',
    participants: ['Public Works', 'Health', 'Transport', 'Revenue', 'Police'],
    status: 'Scheduled'
  },
  {
    key: '2',
    title: 'Emergency Flood Readiness & Equipment Handover Review',
    datetime: 'Nov 14, 2026 at 02:30 PM',
    location: 'Disaster Management Ops Room',
    leadDept: 'Public Works',
    participants: ['Public Works', 'Civil Defense', 'Health'],
    status: 'Scheduled'
  },
  {
    key: '3',
    title: 'Digital Governance & Citizen Grievance SLA Review',
    datetime: 'Nov 17, 2026 at 11:00 AM',
    location: 'Virtual / Teams Room 3',
    leadDept: 'IT & Digital Services',
    participants: ['All Departments'],
    status: 'Scheduled'
  }
];

// Official Memos
const initialMemos = [
  {
    key: '1',
    memoId: 'MEMO-2026-089',
    title: 'Mandatory Submission of Winter Fuel and Generator Readiness Audits',
    from: 'District Magistrate Office',
    to: 'Public Works, Health & Education',
    priority: 'Urgent',
    date: '2026-11-08',
    acknowledged: false
  },
  {
    key: '2',
    memoId: 'MEMO-2026-084',
    title: 'Coordinated Road Restoration Post Fiber-Optic Cable Laying',
    from: 'IT & Digital Services',
    to: 'Public Works & Transportation',
    priority: 'Normal',
    date: '2026-11-05',
    acknowledged: true
  },
  {
    key: '3',
    memoId: 'MEMO-2026-079',
    title: 'Expedited Approval of Waste Segregation Depots in Wards 4 & 7',
    from: 'Health & Sanitation',
    to: 'Urban Planning & Environment',
    priority: 'High',
    date: '2026-11-02',
    acknowledged: true
  }
];

const DepartmentCoordination = () => {
  const [projects, setProjects] = useState(initialProjects);
  const [meetings, setMeetings] = useState(initialMeetings);
  const [memos, setMemos] = useState(initialMemos);
  
  const [memoModalVisible, setMemoModalVisible] = useState(false);
  const [meetingModalVisible, setMeetingModalVisible] = useState(false);
  
  const [memoForm] = Form.useForm();
  const [meetingForm] = Form.useForm();

  const handleCreateMemo = (values) => {
    const newMemo = {
      key: `${Date.now()}`,
      memoId: `MEMO-2026-${Math.floor(100 + Math.random() * 900)}`,
      title: values.title,
      from: values.from || 'Public Works',
      to: values.to,
      priority: values.priority || 'Normal',
      date: new Date().toISOString().split('T')[0],
      acknowledged: false
    };
    setMemos([newMemo, ...memos]);
    message.success(`Official memo ${newMemo.memoId} dispatched to recipient departments.`);
    setMemoModalVisible(false);
    memoForm.resetFields();
  };

  const handleCreateMeeting = (values) => {
    const newMeeting = {
      key: `${Date.now()}`,
      title: values.title,
      datetime: values.datetime || 'Next Week',
      location: values.location || 'Conference Room A',
      leadDept: values.leadDept || 'Administration',
      participants: values.participants ? values.participants.split(',').map(s => s.trim()) : ['Public Works', 'Health'],
      status: 'Scheduled'
    };
    setMeetings([...meetings, newMeeting]);
    message.success('Coordination conference successfully scheduled.');
    setMeetingModalVisible(false);
    meetingForm.resetFields();
  };

  const toggleAcknowledge = (key) => {
    setMemos(memos.map(m => m.key === key ? { ...m, acknowledged: true } : m));
    message.success('Receipt acknowledged. Transmitted to sender.');
  };

  const projectColumns = [
    { title: 'Joint Initiative', dataIndex: 'name', key: 'name', render: t => <strong>{t}</strong> },
    { title: 'Lead Department', dataIndex: 'lead', key: 'lead', render: l => <Tag color="blue">{l}</Tag> },
    { 
      title: 'Partner Departments', 
      dataIndex: 'departments', 
      key: 'departments', 
      render: depts => (
        <Space size={[0, 4]} wrap>
          {depts.map(d => <Tag key={d} color="geekblue">{d}</Tag>)}
        </Space>
      )
    },
    { 
      title: 'Milestone Progress', 
      key: 'progress', 
      render: (_, r) => (
        <Progress 
          percent={r.progress} 
          size="small" 
          status={r.status === 'Completed' ? 'success' : 'active'}
        />
      )
    },
    { title: 'Target Completion', dataIndex: 'deadline', key: 'deadline' },
    { title: 'Joint Budget', dataIndex: 'budget', key: 'budget' }
  ];

  const meetingColumns = [
    { title: 'Conference Topic', dataIndex: 'title', key: 'title', render: t => <strong>{t}</strong> },
    { title: 'Schedule', dataIndex: 'datetime', key: 'datetime', render: d => <span><CalendarOutlined style={{ marginRight: 6 }} />{d}</span> },
    { title: 'Venue', dataIndex: 'location', key: 'location' },
    { title: 'Convening Department', dataIndex: 'leadDept', key: 'leadDept', render: ld => <Tag color="purple">{ld}</Tag> },
    { 
      title: 'Invited Departments', 
      dataIndex: 'participants', 
      key: 'participants',
      render: parts => parts.map(p => <Tag key={p}>{p}</Tag>)
    },
    {
      title: 'Action',
      key: 'action',
      render: () => <Button size="small" type="link">Join / Agenda</Button>
    }
  ];

  const memoColumns = [
    { title: 'Memo ID', dataIndex: 'memoId', key: 'memoId', render: id => <Tag color="cyan">{id}</Tag> },
    { title: 'Subject', dataIndex: 'title', key: 'title', render: s => <strong>{s}</strong> },
    { title: 'Originator', dataIndex: 'from', key: 'from' },
    { title: 'Recipients', dataIndex: 'to', key: 'to' },
    { 
      title: 'Priority', 
      dataIndex: 'priority', 
      key: 'priority', 
      render: p => <Tag color={p === 'Urgent' ? 'red' : p === 'High' ? 'orange' : 'blue'}>{p}</Tag> 
    },
    { title: 'Issued On', dataIndex: 'date', key: 'date' },
    {
      title: 'Status',
      key: 'status',
      render: (_, record) => record.acknowledged ? (
        <Tag color="green" icon={<CheckCircleOutlined />}>Acknowledged</Tag>
      ) : (
        <Button size="small" type="primary" onClick={() => toggleAcknowledge(record.key)}>
          Acknowledge
        </Button>
      )
    }
  ];

  const tabItems = [
    {
      key: '1',
      label: 'Cross-Department Initiatives',
      children: (
        <Card 
          title="Active Multi-Department Collaboration Portfolios"
          extra={<Tag color="green">4 Collaborative Workflows Active</Tag>}
        >
          <Table dataSource={projects} columns={projectColumns} pagination={false} size="middle" />
        </Card>
      )
    },
    {
      key: '2',
      label: 'Inter-Department Meetings',
      children: (
        <Card 
          title="Scheduled Coordination Conferences & Taskforce Sessions"
          extra={<Button type="primary" icon={<PlusOutlined />} onClick={() => setMeetingModalVisible(true)}>Convene Meeting</Button>}
        >
          <Table dataSource={meetings} columns={meetingColumns} pagination={false} size="middle" />
        </Card>
      )
    },
    {
      key: '3',
      label: 'Official Memos & Directives',
      children: (
        <Card 
          title="Inter-Office Directives, Circulars & Approvals"
          extra={<Button type="primary" icon={<SendOutlined />} onClick={() => setMemoModalVisible(true)}>Issue Directive</Button>}
        >
          <Table dataSource={memos} columns={memoColumns} pagination={false} size="middle" />
        </Card>
      )
    },
    {
      key: '4',
      label: 'Coordination Activity Timeline',
      children: (
        <Row gutter={[16, 16]}>
          <Col xs={24} lg={16}>
            <Card title="Recent Cross-Agency Milestones">
              <Timeline
                items={[
                  {
                    color: 'green',
                    children: (
                      <div>
                        <strong>Health & Sanitation signed off with Education</strong>
                        <div style={{ color: '#8c8c8c', fontSize: 12 }}>Nov 09, 2026 - 16:40</div>
                        <p>Completed water quality and sanitation testing across all 42 primary district schools.</p>
                      </div>
                    )
                  },
                  {
                    color: 'blue',
                    children: (
                      <div>
                        <strong>Transportation & IT initiated Fiber Synchronization</strong>
                        <div style={{ color: '#8c8c8c', fontSize: 12 }}>Nov 08, 2026 - 11:15</div>
                        <p>Joint inspection for laying smart bus corridor traffic sensors along Ring Road.</p>
                      </div>
                    )
                  },
                  {
                    color: 'orange',
                    children: (
                      <div>
                        <strong>Public Works requested emergency suction pumps from Civil Defense</strong>
                        <div style={{ color: '#8c8c8c', fontSize: 12 }}>Nov 06, 2026 - 09:20</div>
                        <p>Pre-emptive transfer of 4 heavy-duty diesel suction units ahead of anticipated rain.</p>
                      </div>
                    )
                  },
                  {
                    color: 'purple',
                    children: (
                      <div>
                        <strong>Revenue & Urban Planning GIS Map Integration Milestone #2 Reached</strong>
                        <div style={{ color: '#8c8c8c', fontSize: 12 }}>Nov 03, 2026 - 14:00</div>
                        <p>Mapped 14,200 additional commercial land parcels in Ward 6.</p>
                      </div>
                    )
                  }
                ]}
              />
            </Card>
          </Col>
          <Col xs={24} lg={8}>
            <Card title="Coordination Health Scorecard">
              <div style={{ textAlign: 'center', padding: '16px 0' }}>
                <Progress type="circle" percent={91} strokeColor="#52c41a" />
                <h3 style={{ marginTop: 16 }}>High Synergy Index</h3>
                <p style={{ color: '#8c8c8c' }}>Average inter-department memo turnaround is currently 3.4 hours.</p>
              </div>
            </Card>
          </Col>
        </Row>
      )
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>Department Coordination & Inter-Agency Hub</h1>
          <span style={{ color: '#8c8c8c' }}>Cross-functional joint projects, inter-office directives, and taskforce synchronization</span>
        </div>
        <Space>
          <Button icon={<CalendarOutlined />} onClick={() => setMeetingModalVisible(true)}>Schedule Meeting</Button>
          <Button type="primary" icon={<SendOutlined />} onClick={() => setMemoModalVisible(true)}>Issue Memo</Button>
        </Space>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f0f5ff', borderColor: '#adc6ff' }}>
            <Statistic
              title="Active Joint Initiatives"
              value={projects.filter(p => p.status === 'In Progress').length}
              suffix={`/ ${projects.length} Total`}
              prefix={<TeamOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1d39c4', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>Cross-agency taskforces active</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed', borderColor: '#b7eb8f' }}>
            <Statistic
              title="Avg Inter-Agency Turnaround"
              value={3.4}
              suffix="hrs"
              prefix={<ClockCircleOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#389e0d', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>Fast response to inter-office requests</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff7e6', borderColor: '#ffd591' }}>
            <Statistic
              title="Pending Memo Acknowledgments"
              value={memos.filter(m => !m.acknowledged).length}
              prefix={<ExclamationCircleOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#d46b08', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#faad14' }}>Action items awaiting sign-off</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f9f0ff', borderColor: '#d3adf7' }}>
            <Statistic
              title="Upcoming Steering Sessions"
              value={meetings.length}
              prefix={<CalendarOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#531dab', fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#722ed1' }}>Convened this fortnight</div>
          </Card>
        </Col>
      </Row>

      <Tabs activeKey={tabItems[0].key} items={tabItems} />

      <Modal
        title="Issue Inter-Office Directive / Memo"
        open={memoModalVisible}
        onCancel={() => setMemoModalVisible(false)}
        footer={null}
      >
        <Form form={memoForm} layout="vertical" onFinish={handleCreateMemo}>
          <Form.Item name="title" label="Directive / Subject" rules={[{ required: true, message: 'Please specify subject' }]}>
            <Input placeholder="e.g. Expedited Clearance of Storm Drains along Rail Line" />
          </Form.Item>
          <Form.Item name="from" label="Issuing Department" initialValue="Public Works">
            <Select>
              <Option value="Public Works">Public Works</Option>
              <Option value="Health & Sanitation">Health & Sanitation</Option>
              <Option value="Transportation">Transportation</Option>
              <Option value="District Magistrate Office">District Magistrate Office</Option>
            </Select>
          </Form.Item>
          <Form.Item name="to" label="Target Recipient Department(s)" rules={[{ required: true, message: 'Specify target department' }]}>
            <Input placeholder="e.g. Health & Sanitation, Urban Planning" />
          </Form.Item>
          <Form.Item name="priority" label="Priority Level" initialValue="Normal">
            <Select>
              <Option value="Normal">Normal</Option>
              <Option value="High">High</Option>
              <Option value="Urgent">Urgent / Immediate Action</Option>
            </Select>
          </Form.Item>
          <div style={{ textAlign: 'right', marginTop: 16 }}>
            <Space>
              <Button onClick={() => setMemoModalVisible(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit">Dispatch Memo</Button>
            </Space>
          </div>
        </Form>
      </Modal>

      <Modal
        title="Schedule Cross-Agency Coordination Session"
        open={meetingModalVisible}
        onCancel={() => setMeetingModalVisible(false)}
        footer={null}
      >
        <Form form={meetingForm} layout="vertical" onFinish={handleCreateMeeting}>
          <Form.Item name="title" label="Conference Topic / Objective" rules={[{ required: true, message: 'Specify meeting title' }]}>
            <Input placeholder="e.g. Winter Air Quality & Traffic Decongestion Steering" />
          </Form.Item>
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="datetime" label="Date & Time" initialValue="Nov 20, 2026 at 11:00 AM">
                <Input placeholder="e.g. Nov 20, 2026 at 11:00 AM" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="location" label="Location / Room" initialValue="Conference Room 2">
                <Input placeholder="Room or Video Link" />
              </Form.Item>
            </Col>
          </Row>
          <Form.Item name="participants" label="Participating Departments (comma separated)" initialValue="Public Works, Transportation, Environment">
            <Input />
          </Form.Item>
          <div style={{ textAlign: 'right', marginTop: 16 }}>
            <Space>
              <Button onClick={() => setMeetingModalVisible(false)}>Cancel</Button>
              <Button type="primary" htmlType="submit">Convene Session</Button>
            </Space>
          </div>
        </Form>
      </Modal>
    </div>
  );
};

export default DepartmentCoordination;
