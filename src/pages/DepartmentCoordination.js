import React, { useState } from 'react';
import { Card, Row, Col, Table, Button, Modal, Form, Input, Select, Tag, Timeline, Tabs, Space, Badge, Alert } from 'antd';
import { MessageOutlined, TeamOutlined, ShareAltOutlined, ClockCircleOutlined, SendOutlined, PlusOutlined } from '@ant-design/icons';

const { Option } = Select;
const { TextArea } = Input;
const { TabPane } = Tabs;

const DepartmentCoordination = () => {
  const [messageModalVisible, setMessageModalVisible] = useState(false);
  const [meetingModalVisible, setMeetingModalVisible] = useState(false);
  const [form] = Form.useForm();

  const departments = ['Public Works', 'Health', 'Education', 'Finance', 'Transportation', 'Environment', 'Social Services', 'Planning', 'Legal', 'IT'];

  const collaborationColumns = [
    { title: 'Project Name', dataIndex: 'name', key: 'name' },
    { title: 'Departments', dataIndex: 'departments', key: 'departments', render: (depts) => depts?.map(dept => <Tag key={dept}>{dept}</Tag>) },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (status) => <Tag color={status === 'Active' ? 'green' : 'orange'}>{status}</Tag> },
    { title: 'Progress', dataIndex: 'progress', key: 'progress', render: (progress) => `${progress || 0}%` },
    { title: 'Lead Department', dataIndex: 'lead', key: 'lead' },
    { title: 'Deadline', dataIndex: 'deadline', key: 'deadline' },
    { title: 'Actions', key: 'actions', render: () => <Space><Button size="small">View</Button><Button size="small">Update</Button></Space> }
  ];

  const meetingColumns = [
    { title: 'Meeting Title', dataIndex: 'title', key: 'title' },
    { title: 'Date & Time', dataIndex: 'datetime', key: 'datetime' },
    { title: 'Participants', dataIndex: 'participants', key: 'participants', render: (count) => <Badge count={count || 0} /> },
    { title: 'Department', dataIndex: 'department', key: 'department' },
    { title: 'Status', dataIndex: 'status', key: 'status', render: (status) => <Tag color={status === 'Scheduled' ? 'blue' : status === 'Completed' ? 'green' : 'orange'}>{status}</Tag> },
    { title: 'Actions', key: 'actions', render: () => <Space><Button size="small">Join</Button><Button size="small">Details</Button></Space> }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1>Department Coordination</h1>
        <Space>
          <Button type="primary" icon={<MessageOutlined />} onClick={() => setMessageModalVisible(true)}>Send Message</Button>
          <Button icon={<TeamOutlined />} onClick={() => setMeetingModalVisible(true)}>Schedule Meeting</Button>
        </Space>
      </div>

      <Alert
        message="Coordination Platform"
        description="Connect to your organization's communication systems to enable real-time inter-departmental collaboration and workflow management."
        type="info"
        showIcon
        style={{ marginBottom: '24px' }}
      />

      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col span={6}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <MessageOutlined style={{ fontSize: '24px', color: '#1890ff' }} />
              <div style={{ marginTop: '8px', fontSize: '24px', fontWeight: 'bold' }}>0</div>
              <div style={{ color: '#666' }}>Active Messages</div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <TeamOutlined style={{ fontSize: '24px', color: '#52c41a' }} />
              <div style={{ marginTop: '8px', fontSize: '24px', fontWeight: 'bold' }}>0</div>
              <div style={{ color: '#666' }}>Ongoing Projects</div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <ClockCircleOutlined style={{ fontSize: '24px', color: '#faad14' }} />
              <div style={{ marginTop: '8px', fontSize: '24px', fontWeight: 'bold' }}>0</div>
              <div style={{ color: '#666' }}>Scheduled Meetings</div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <div style={{ textAlign: 'center' }}>
              <ShareAltOutlined style={{ fontSize: '24px', color: '#722ed1' }} />
              <div style={{ marginTop: '8px', fontSize: '24px', fontWeight: 'bold' }}>0</div>
              <div style={{ color: '#666' }}>Shared Resources</div>
            </div>
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="1">
        <TabPane tab="Messages & Communication" key="1">
          <Row gutter={16}>
            <Col span={16}>
              <Card title="Department Messages">
                <div style={{ height: '400px', padding: '20px', textAlign: 'center', color: '#666' }}>
                  <MessageOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
                  <div>Connect to your messaging system to view department communications</div>
                  <div style={{ fontSize: '12px', marginTop: '8px' }}>Supports integration with Slack, Microsoft Teams, and email systems</div>
                </div>
              </Card>
            </Col>
            <Col span={8}>
              <Card title="Quick Actions">
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Button block icon={<MessageOutlined />}>Broadcast Message</Button>
                  <Button block icon={<TeamOutlined />}>Create Group Chat</Button>
                  <Button block icon={<ShareAltOutlined />}>Share Document</Button>
                  <Button block icon={<ClockCircleOutlined />}>Schedule Update</Button>
                </Space>
              </Card>
              
              <Card title="Online Departments" style={{ marginTop: '16px' }}>
                <div style={{ padding: '10px', textAlign: 'center', color: '#666' }}>
                  Department status will display here when connected to communication systems
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Collaborative Projects" key="2">
          <Card title="Inter-Department Projects">
            <Table dataSource={[]} columns={collaborationColumns} pagination={{ pageSize: 10 }} locale={{ emptyText: 'No collaborative projects found. Connect to project management system.' }} />
          </Card>
        </TabPane>

        <TabPane tab="Meetings & Events" key="3">
          <Card title="Scheduled Meetings">
            <Table dataSource={[]} columns={meetingColumns} pagination={{ pageSize: 10 }} locale={{ emptyText: 'No meetings scheduled. Connect to calendar system.' }} />
          </Card>
        </TabPane>

        <TabPane tab="Workflow Management" key="4">
          <Row gutter={16}>
            <Col span={12}>
              <Card title="Cross-Department Workflows">
                <div style={{ height: '350px', padding: '20px', textAlign: 'center', color: '#666' }}>
                  Workflow management and approval processes will display here
                </div>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="Process Timeline">
                <Timeline style={{ padding: '20px' }}>
                  <Timeline.Item color="gray">Connect workflow management system to view process timelines</Timeline.Item>
                </Timeline>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Document Sharing" key="5">
          <Row gutter={16}>
            <Col span={16}>
              <Card title="Shared Documents">
                <Table 
                  dataSource={[]} 
                  columns={[
                    { title: 'Document Name', dataIndex: 'name', key: 'name' },
                    { title: 'Department', dataIndex: 'department', key: 'department' },
                    { title: 'Shared With', dataIndex: 'sharedWith', key: 'sharedWith' },
                    { title: 'Last Modified', dataIndex: 'modified', key: 'modified' },
                    { title: 'Actions', key: 'actions', render: () => <Space><Button size="small">View</Button><Button size="small">Download</Button></Space> }
                  ]} 
                  pagination={{ pageSize: 8 }} 
                  locale={{ emptyText: 'No shared documents. Connect to document management system.' }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card title="Upload Document">
                <Form layout="vertical">
                  <Form.Item label="Document Title">
                    <Input placeholder="Enter document title" />
                  </Form.Item>
                  <Form.Item label="Share With Departments">
                    <Select mode="multiple" placeholder="Select departments">
                      {departments.map(dept => <Option key={dept} value={dept}>{dept}</Option>)}
                    </Select>
                  </Form.Item>
                  <Form.Item label="Access Level">
                    <Select placeholder="Select access level">
                      <Option value="view">View Only</Option>
                      <Option value="edit">Edit Access</Option>
                      <Option value="admin">Admin Access</Option>
                    </Select>
                  </Form.Item>
                  <Button type="primary" block disabled>Upload Document</Button>
                </Form>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Activity Feed" key="6">
          <Card title="Department Activity">
            <Timeline>
              <Timeline.Item color="gray">
                Connect to activity tracking systems to view real-time department updates and notifications
              </Timeline.Item>
            </Timeline>
          </Card>
        </TabPane>
      </Tabs>

      <Modal title="Send Message" open={messageModalVisible} onCancel={() => setMessageModalVisible(false)} footer={null}>
        <Form form={form} layout="vertical">
          <Form.Item label="Recipients" name="recipients" rules={[{ required: true, message: 'Please select recipients' }]}>
            <Select mode="multiple" placeholder="Select departments or individuals">
              {departments.map(dept => <Option key={dept} value={dept}>{dept}</Option>)}
            </Select>
          </Form.Item>
          <Form.Item label="Subject" name="subject" rules={[{ required: true, message: 'Please enter subject' }]}>
            <Input placeholder="Enter message subject" />
          </Form.Item>
          <Form.Item label="Message" name="message" rules={[{ required: true, message: 'Please enter message' }]}>
            <TextArea rows={4} placeholder="Enter your message" />
          </Form.Item>
          <Form.Item label="Priority" name="priority">
            <Select placeholder="Select priority">
              <Option value="low">Low</Option>
              <Option value="medium">Medium</Option>
              <Option value="high">High</Option>
              <Option value="urgent">Urgent</Option>
            </Select>
          </Form.Item>
          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Button onClick={() => setMessageModalVisible(false)} style={{ marginRight: 8 }}>Cancel</Button>
            <Button type="primary" icon={<SendOutlined />}>Send Message</Button>
          </Form.Item>
        </Form>
      </Modal>

      <Modal title="Schedule Meeting" open={meetingModalVisible} onCancel={() => setMeetingModalVisible(false)} footer={null}>
        <Form form={form} layout="vertical">
          <Form.Item label="Meeting Title" name="title" rules={[{ required: true, message: 'Please enter meeting title' }]}>
            <Input placeholder="Enter meeting title" />
          </Form.Item>
          <Form.Item label="Participants" name="participants" rules={[{ required: true, message: 'Please select participants' }]}>
            <Select mode="multiple" placeholder="Select departments or individuals">
              {departments.map(dept => <Option key={dept} value={dept}>{dept}</Option>)}
            </Select>
          </Form.Item>
          <Form.Item label="Date & Time" name="datetime" rules={[{ required: true, message: 'Please select date and time' }]}>
            <Input type="datetime-local" />
          </Form.Item>
          <Form.Item label="Duration" name="duration">
            <Select placeholder="Select duration">
              <Option value="30">30 minutes</Option>
              <Option value="60">1 hour</Option>
              <Option value="90">1.5 hours</Option>
              <Option value="120">2 hours</Option>
            </Select>
          </Form.Item>
          <Form.Item label="Meeting Link" name="link">
            <Input placeholder="Video conference link (optional)" />
          </Form.Item>
          <Form.Item label="Agenda" name="agenda">
            <TextArea rows={3} placeholder="Meeting agenda" />
          </Form.Item>
          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Button onClick={() => setMeetingModalVisible(false)} style={{ marginRight: 8 }}>Cancel</Button>
            <Button type="primary" icon={<PlusOutlined />}>Schedule Meeting</Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DepartmentCoordination;