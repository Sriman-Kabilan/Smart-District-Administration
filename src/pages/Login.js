import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Spin } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

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

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px'
    }}>
      <Card 
        title="District Administration Login" 
        style={{
          width: '400px',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.12)',
          borderRadius: '12px'
        }}
        headStyle={{
          textAlign: 'center',
          fontSize: '20px',
          fontWeight: 'bold',
          borderBottom: '1px solid #f0f0f0'
        }}
      >
        <Form
          name="login"
          onFinish={onFinish}
          layout="vertical"
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: 'Please enter your username!' }]}
          >
            <Input 
              prefix={<UserOutlined />} 
              placeholder="Username" 
              size="large"
            />
          </Form.Item>
          
          <Form.Item
            name="password"
            rules={[{ required: true, message: 'Please enter your password!' }]}
          >
            <Input.Password 
              prefix={<LockOutlined />} 
              placeholder="Password" 
              size="large"
            />
          </Form.Item>
          
          <Form.Item>
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading}
              size="large"
              block
            >
              Login
            </Button>
          </Form.Item>
        </Form>
        
        <div style={{ marginTop: 24, padding: 16, backgroundColor: '#f8f9fa', borderRadius: 8 }}>
          <h4 style={{ margin: 0, marginBottom: 12, color: '#495057', fontSize: '14px' }}>Demo Credentials:</h4>
          <div style={{ fontSize: '12px', color: '#6c757d' }}>
            <div style={{ marginBottom: 8 }}>
              <strong>Administrator:</strong> admin / admin123
            </div>
            <div style={{ marginBottom: 8 }}>
              <strong>Department Head:</strong> dept_head / dept123
            </div>
            <div>
              <strong>Staff Member:</strong> staff / staff123
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Login;