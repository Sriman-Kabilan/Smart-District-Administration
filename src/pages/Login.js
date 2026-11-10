import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Space, Divider } from 'antd';
import { UserOutlined, LockOutlined, SafetyCertificateOutlined } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form] = Form.useForm();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await login(values.username, values.password);
      message.success('Welcome to District Administration Dashboard!');
      navigate('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      if (error.response?.status === 401) {
        message.error('Invalid username or password');
      } else if (error.response?.status >= 500) {
        message.error('Server error. Please try again later.');
      } else if (error.code === 'NETWORK_ERROR') {
        message.error('Unable to connect to server. Please check your connection.');
      } else {
        message.error('Login failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = (username, password) => {
    form.setFieldsValue({ username, password });
    onFinish({ username, password });
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #1890ff 0%, #001529 100%)',
      padding: '20px'
    }}>
      <Card 
        title={
          <div style={{ textAlign: 'center', padding: '8px 0' }}>
            <SafetyCertificateOutlined style={{ fontSize: 32, color: '#1890ff', marginBottom: 8 }} />
            <div style={{ fontSize: 20, fontWeight: 700 }}>Smart District Administration</div>
            <div style={{ fontSize: 13, color: '#8c8c8c', fontWeight: 400 }}>Official Municipal Command Portal</div>
          </div>
        }
        style={{
          width: '420px',
          boxShadow: '0 12px 40px rgba(0, 0, 0, 0.25)',
          borderRadius: '12px'
        }}
      >
        <Form
          form={form}
          name="login"
          onFinish={onFinish}
          layout="vertical"
        >
          <Form.Item
            name="username"
            label="Officer Username"
            rules={[{ required: true, message: 'Please enter your username' }]}
          >
            <Input 
              prefix={<UserOutlined style={{ color: '#1890ff' }} />} 
              placeholder="Username" 
              size="large"
            />
          </Form.Item>
          
          <Form.Item
            name="password"
            label="Secure Passkey"
            rules={[{ required: true, message: 'Please enter your passkey' }]}
          >
            <Input.Password 
              prefix={<LockOutlined style={{ color: '#1890ff' }} />} 
              placeholder="Password" 
              size="large"
            />
          </Form.Item>
          
          <Form.Item style={{ marginBottom: 12 }}>
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading}
              size="large"
              block
              style={{ height: 44, fontWeight: 600 }}
            >
              Sign In to Command Portal
            </Button>
          </Form.Item>
        </Form>
        
        <Divider style={{ margin: '16px 0 12px 0', fontSize: 12, color: '#8c8c8c' }}>
          One-Click Demo Roles
        </Divider>

        <Space direction="vertical" style={{ width: '100%' }}>
          <Button 
            block 
            style={{ textAlign: 'left', background: '#f0f5ff', borderColor: '#adc6ff' }}
            onClick={() => handleQuickLogin('admin', 'admin123')}
          >
            🔑 <strong>Administrator</strong> (admin / admin123)
          </Button>
          <Button 
            block 
            style={{ textAlign: 'left', background: '#f6ffed', borderColor: '#b7eb8f' }}
            onClick={() => handleQuickLogin('dept_head', 'dept123')}
          >
            🏢 <strong>Department Head</strong> (dept_head / dept123)
          </Button>
          <Button 
            block 
            style={{ textAlign: 'left', background: '#fff7e6', borderColor: '#ffd591' }}
            onClick={() => handleQuickLogin('staff', 'staff123')}
          >
            👷 <strong>Staff Member</strong> (staff / staff123)
          </Button>
        </Space>
      </Card>
    </div>
  );
};

export default Login;
