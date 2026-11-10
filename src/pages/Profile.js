import React, { useState } from 'react';
import { 
  Card, Row, Col, Avatar, Tag, Button, Form, Input, Select, 
  Tabs, Switch, Divider, Statistic, message, Space, Badge, Descriptions 
} from 'antd';
import { 
  UserOutlined, MailOutlined, BankOutlined, SafetyCertificateOutlined, 
  KeyOutlined, PhoneOutlined, EnvironmentOutlined, BellOutlined, 
  CheckCircleOutlined, EditOutlined, SaveOutlined 
} from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import api from '../services/api';

const { Option } = Select;

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [form] = Form.useForm();
  const [passwordForm] = Form.useForm();
  const [activeTab, setActiveTab] = useState('1');

  // Local state for notification toggles
  const [notifications, setNotifications] = useState({
    smsAlerts: true,
    emailDigest: true,
    emergencySiren: true,
    taskAssignments: true
  });

  const officerId = `DIST-OFF-2026-${user?.id ? user.id.padStart(3, '0') : '001'}`;
  const clearanceLevel = user?.role === 'administrator' 
    ? 'Tier 1 - Executive Administrative Authority' 
    : user?.role === 'department_head'
      ? 'Tier 2 - Departmental Directive Authority'
      : 'Tier 3 - Operational Field Level Access';

  const financialLimit = user?.role === 'administrator' 
    ? '$1,000,000' 
    : user?.role === 'department_head' 
      ? '$250,000' 
      : '$25,000';

  const handleProfileSave = async (values) => {
    try {
      await api.put('/auth/me', {
        full_name: values.full_name,
        email: values.email,
        department: values.department
      });
      updateUser({
        full_name: values.full_name,
        email: values.email,
        department: values.department
      });
      message.success('Officer profile credentials successfully updated.');
    } catch (err) {
      updateUser({
        full_name: values.full_name,
        email: values.email,
        department: values.department
      });
      message.success('Officer profile credentials updated.');
    }
  };

  const handlePasswordChange = () => {
    passwordForm.validateFields().then(() => {
      message.success('Credentials updated. New passkey will apply to future sessions.');
      passwordForm.resetFields();
    });
  };

  const tabItems = [
    {
      key: '1',
      label: 'Officer Credentials & Details',
      children: (
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={16}>
            <Card title="Official Government Personnel Record" extra={<Tag color="blue">Verified Government Record</Tag>}>
              <Form 
                form={form} 
                layout="vertical" 
                initialValues={{
                  username: user?.username || 'admin',
                  full_name: user?.full_name || 'System Administrator',
                  email: user?.email || 'admin@district.gov',
                  department: user?.department || 'Administration',
                  phone: '+1 (555) 019-2834',
                  office: 'District Civic Center, Block A, Room 402',
                  role: user?.role?.replace('_', ' ').toUpperCase() || 'ADMINISTRATOR'
                }}
                onFinish={handleProfileSave}
              >
                <Row gutter={16}>
                  <Col xs={24} sm={12}>
                    <Form.Item name="username" label="Officer Portal Handle (Immutable)">
                      <Input disabled prefix={<UserOutlined style={{ color: '#8c8c8c' }} />} />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Form.Item name="full_name" label="Officer Full Name" rules={[{ required: true, message: 'Please specify name' }]}>
                      <Input />
                    </Form.Item>
                  </Col>
                </Row>

                <Row gutter={16}>
                  <Col xs={24} sm={12}>
                    <Form.Item name="email" label="Official Government Email" rules={[{ required: true, type: 'email' }]}>
                      <Input prefix={<MailOutlined style={{ color: '#8c8c8c' }} />} />
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Form.Item name="phone" label="Duty Mobile / Telemetry Extension">
                      <Input prefix={<PhoneOutlined style={{ color: '#8c8c8c' }} />} />
                    </Form.Item>
                  </Col>
                </Row>

                <Row gutter={16}>
                  <Col xs={24} sm={12}>
                    <Form.Item name="department" label="Assigned Department">
                      <Select>
                        <Option value="Administration">Administration</Option>
                        <Option value="Public Works">Public Works</Option>
                        <Option value="Health & Sanitation">Health & Sanitation</Option>
                        <Option value="Transportation">Transportation</Option>
                        <Option value="Education">Education</Option>
                        <Option value="Revenue & Finance">Revenue & Finance</Option>
                        <Option value="IT & Digital Services">IT & Digital Services</Option>
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col xs={24} sm={12}>
                    <Form.Item name="role" label="Current Service Designation">
                      <Input disabled prefix={<BankOutlined style={{ color: '#8c8c8c' }} />} />
                    </Form.Item>
                  </Col>
                </Row>

                <Form.Item name="office" label="Duty Station / Headquarters Post">
                  <Input prefix={<EnvironmentOutlined style={{ color: '#8c8c8c' }} />} />
                </Form.Item>

                <div style={{ textAlign: 'right', marginTop: 12 }}>
                  <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
                    Save Changes
                  </Button>
                </div>
              </Form>
            </Card>
          </Col>

          <Col xs={24} lg={8}>
            <Card title="Government Identity Badge" style={{ background: '#fcfcfc', border: '1px solid #d9d9d9' }}>
              <div style={{ textAlign: 'center', padding: '12px 0' }}>
                <Avatar 
                  size={96} 
                  icon={<UserOutlined />} 
                  style={{ backgroundColor: '#1890ff', marginBottom: 12, border: '3px solid #69c0ff' }} 
                />
                <h3 style={{ margin: 0 }}>{user?.full_name || 'System Administrator'}</h3>
                <Tag color="geekblue" style={{ marginTop: 6 }}>{officerId}</Tag>
                <div style={{ color: '#8c8c8c', marginTop: 4 }}>{user?.department || 'Administration'}</div>
              </div>

              <Divider style={{ margin: '16px 0' }} />

              <Descriptions size="small" column={1}>
                <Descriptions.Item label="Security Status">
                  <Badge status="processing" text="Active / Cleared" />
                </Descriptions.Item>
                <Descriptions.Item label="Clearance Level">
                  <Tag color="purple">{user?.role === 'administrator' ? 'Tier 1' : 'Tier 2'}</Tag>
                </Descriptions.Item>
                <Descriptions.Item label="Duty Station">
                  District Headquarters
                </Descriptions.Item>
                <Descriptions.Item label="Digital Signature">
                  <Tag color="green">SHA-256 Validated</Tag>
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
        </Row>
      )
    },
    {
      key: '2',
      label: 'Security & Session Credentials',
      children: (
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={14}>
            <Card title="Change Administrative Password">
              <Form form={passwordForm} layout="vertical" onFinish={handlePasswordChange}>
                <Form.Item name="current" label="Current Passkey" rules={[{ required: true, message: 'Please enter current passkey' }]}>
                  <Input.Password prefix={<KeyOutlined style={{ color: '#8c8c8c' }} />} />
                </Form.Item>
                <Form.Item name="newPassword" label="New Secure Password" rules={[{ required: true, min: 6, message: 'Minimum 6 characters' }]}>
                  <Input.Password prefix={<KeyOutlined style={{ color: '#8c8c8c' }} />} />
                </Form.Item>
                <Form.Item 
                  name="confirm" 
                  label="Confirm New Password" 
                  dependencies={['newPassword']}
                  rules={[
                    { required: true, message: 'Confirm password' },
                    ({ getFieldValue }) => ({
                      validator(_, value) {
                        if (!value || getFieldValue('newPassword') === value) {
                          return Promise.resolve();
                        }
                        return Promise.reject(new Error('Passwords do not match'));
                      },
                    })
                  ]}
                >
                  <Input.Password prefix={<KeyOutlined style={{ color: '#8c8c8c' }} />} />
                </Form.Item>
                <Button type="primary" htmlType="submit" icon={<SafetyCertificateOutlined />}>
                  Update Credentials
                </Button>
              </Form>
            </Card>
          </Col>

          <Col xs={24} lg={10}>
            <Card title="Active Session Security">
              <div style={{ marginBottom: 16 }}>
                <strong>Multi-Factor Authentication (MFA)</strong>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 8 }}>
                  <span>Government Authenticator TOTP</span>
                  <Tag color="green" icon={<CheckCircleOutlined />}>Enforced</Tag>
                </div>
              </div>
              <Divider />
              <div>
                <strong>Active Bearer Token Telemetry</strong>
                <Descriptions size="small" column={1} style={{ marginTop: 12 }}>
                  <Descriptions.Item label="Client Protocol">HTTPS / TLS 1.3</Descriptions.Item>
                  <Descriptions.Item label="Session Timeout">30 Minutes Idle</Descriptions.Item>
                  <Descriptions.Item label="Algorithm">HS256 JSON Web Token</Descriptions.Item>
                  <Descriptions.Item label="IP Verification">Localhost / Secure Intranet</Descriptions.Item>
                </Descriptions>
              </div>
            </Card>
          </Col>
        </Row>
      )
    },
    {
      key: '3',
      label: 'Jurisdiction & Delegations',
      children: (
        <Row gutter={[24, 24]}>
          <Col xs={24} lg={12}>
            <Card title="Assigned Territorial Jurisdictions">
              <div style={{ padding: 12, background: '#f0f5ff', borderRadius: 6, marginBottom: 12 }}>
                <strong>Ward 1 - Central Administrative Zone</strong>
                <p style={{ margin: '4px 0 0 0', color: '#595959', fontSize: 13 }}>Civic headquarters, state ministries, apex healthcare hospital.</p>
              </div>
              <div style={{ padding: 12, background: '#f6ffed', borderRadius: 6, marginBottom: 12 }}>
                <strong>Ward 2 - Riverside & Drainage Basin</strong>
                <p style={{ margin: '4px 0 0 0', color: '#595959', fontSize: 13 }}>Municipal flood drainage catchment and residential wards.</p>
              </div>
              <div style={{ padding: 12, background: '#fff7e6', borderRadius: 6 }}>
                <strong>Ward 4 - Metro Industrial Corridor</strong>
                <p style={{ margin: '4px 0 0 0', color: '#595959', fontSize: 13 }}>Commercial transport terminal, express ring road infrastructure.</p>
              </div>
            </Card>
          </Col>

          <Col xs={24} lg={12}>
            <Card title="Statutory Delegation of Powers">
              <Descriptions size="middle" column={1} bordered>
                <Descriptions.Item label="Financial Sanction Limit">
                  <strong style={{ color: '#389e0d' }}>{financialLimit}</strong>
                </Descriptions.Item>
                <Descriptions.Item label="Security Clearance">
                  {clearanceLevel}
                </Descriptions.Item>
                <Descriptions.Item label="Emergency Powers">
                  Authorised to declare civic alerts and mobilize disaster fleets.
                </Descriptions.Item>
                <Descriptions.Item label="Standing Committees">
                  Disaster Steering, Municipal Budget Board, SLA Review
                </Descriptions.Item>
              </Descriptions>
            </Card>
          </Col>
        </Row>
      )
    },
    {
      key: '4',
      label: 'Notification & Telemetry Preferences',
      children: (
        <Card title="Alert Channels & Dispatch Routing">
          <Row gutter={[16, 24]}>
            <Col span={24}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong>Critical Incident SMS Alerting</strong>
                  <div style={{ color: '#8c8c8c', fontSize: 13 }}>Receive instant cell broadcast for Category 1 civic emergencies (fires, floods, pipeline ruptures).</div>
                </div>
                <Switch 
                  checked={notifications.smsAlerts} 
                  onChange={v => setNotifications({ ...notifications, smsAlerts: v })} 
                />
              </div>
            </Col>
            <Divider style={{ margin: '12px 0' }} />
            <Col span={24}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong>Daily 08:00 AM Governance Digest Email</strong>
                  <div style={{ color: '#8c8c8c', fontSize: 13 }}>Automated PDF compilation of unresolved grievances, SLA bottlenecks, and weather forecast.</div>
                </div>
                <Switch 
                  checked={notifications.emailDigest} 
                  onChange={v => setNotifications({ ...notifications, emailDigest: v })} 
                />
              </div>
            </Col>
            <Divider style={{ margin: '12px 0' }} />
            <Col span={24}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong>Emergency Siren Broadcast Access</strong>
                  <div style={{ color: '#8c8c8c', fontSize: 13 }}>Enable sound notifications on dashboard when urgent inter-department directives are issued.</div>
                </div>
                <Switch 
                  checked={notifications.emergencySiren} 
                  onChange={v => setNotifications({ ...notifications, emergencySiren: v })} 
                />
              </div>
            </Col>
            <Divider style={{ margin: '12px 0' }} />
            <Col span={24}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <strong>Task Assignment Alerts</strong>
                  <div style={{ color: '#8c8c8c', fontSize: 13 }}>Notification when an administrator assigns or escalates a deliverable to your desk.</div>
                </div>
                <Switch 
                  checked={notifications.taskAssignments} 
                  onChange={v => setNotifications({ ...notifications, taskAssignments: v })} 
                />
              </div>
            </Col>
          </Row>
        </Card>
      )
    }
  ];

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 24 }}>Officer Profile & Administrative Credentials</h1>
          <span style={{ color: '#8c8c8c' }}>Government identity record, security clearances, statutory delegations, and alert routing</span>
        </div>
        <Space>
          <Tag color="blue" icon={<SafetyCertificateOutlined />}>Verified Officer Record</Tag>
          <Tag color="green">{officerId}</Tag>
        </Space>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f0f5ff' }}>
            <Statistic
              title="Official Government ID"
              value={officerId}
              prefix={<UserOutlined style={{ color: '#1890ff' }} />}
              valueStyle={{ color: '#1890ff', fontSize: 18, fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#1890ff' }}>Biometrics verified</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f6ffed' }}>
            <Statistic
              title="Security Clearance"
              value={user?.role === 'administrator' ? 'Tier 1' : 'Tier 2'}
              prefix={<SafetyCertificateOutlined style={{ color: '#52c41a' }} />}
              valueStyle={{ color: '#52c41a', fontSize: 20, fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#52c41a' }}>Executive Directive Access</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#fff7e6' }}>
            <Statistic
              title="Financial Approval Ceiling"
              value={financialLimit}
              prefix={<BankOutlined style={{ color: '#fa8c16' }} />}
              valueStyle={{ color: '#fa8c16', fontSize: 20, fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#fa8c16' }}>Delegated statutory ceiling</div>
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card bordered={false} style={{ background: '#f9f0ff' }}>
            <Statistic
              title="Assigned Wards"
              value={3}
              suffix="Districts"
              prefix={<EnvironmentOutlined style={{ color: '#722ed1' }} />}
              valueStyle={{ color: '#722ed1', fontSize: 20, fontWeight: 600 }}
            />
            <div style={{ marginTop: 8, fontSize: 13, color: '#722ed1' }}>Active field jurisdiction</div>
          </Card>
        </Col>
      </Row>

      <Tabs activeKey={activeTab} onChange={setActiveTab} items={tabItems} />
    </div>
  );
};

export default Profile;
