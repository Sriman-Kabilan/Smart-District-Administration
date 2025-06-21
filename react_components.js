// AuthContext.js - Authentication Context Provider
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/auth';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      authService.getCurrentUser()
        .then(setUser)
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (username, password) => {
    const response = await authService.login(username, password);
    localStorage.setItem('token', response.access_token);
    setUser(response.user);
    return response;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value = {
    user,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// LoginForm.js - Login Component
import React, { useState } from 'react';
import { Form, Input, Button, Card, message, Spin } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginForm = () => {
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      await login(values.username, values.password);
      message.success('Login successful!');
      navigate('/dashboard');
    } catch (error) {
      message.error('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <Card 
        title="District Administration Login" 
        style={{ width: 400, boxShadow: '0 4px 12px rgba(0,0,0,0.15)' }}
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
      </Card>
    </div>
  );
};

// Layout.js - Main Layout Component
import React, { useState } from 'react';
import { Layout as AntLayout, Menu, Avatar, Dropdown, Button } from 'antd';
import { 
  DashboardOutlined, 
  BarChartOutlined, 
  TeamOutlined,
  TasksOutlined,
  GlobalOutlined,
  FileTextOutlined,
  RobotOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined
} from '@ant-design/icons';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';

const { Header, Sider, Content } = AntLayout;

const Layout = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/performance',
      icon: <BarChartOutlined />,
      label: 'Performance Metrics',
    },
    {
      key: '/resources',
      icon: <TeamOutlined />,
      label: 'Resource Management',
    },
    {
      key: '/tasks',
      icon: <TasksOutlined />,
      label: 'Task Tracking',
    },
    {
      key: '/coordination',
      icon: <GlobalOutlined />,
      label: 'Department Coordination',
    },
    {
      key: '/geospatial',
      icon: <GlobalOutlined />,
      label: 'Geospatial View',
    },
    {
      key: '/reports',
      icon: <FileTextOutlined />,
      label: 'Reports',
    },
    {
      key: '/analytics',
      icon: <RobotOutlined />,
      label: 'AI Analytics',
    },
  ];

  const handleMenuClick = ({ key }) => {
    navigate(key);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const userMenu = (
    <Menu>
      <Menu.Item key="profile" icon={<UserOutlined />}>
        Profile
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout}>
        Logout
      </Menu.Item>
    </Menu>
  );

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider trigger={null} collapsible collapsed={collapsed}>
        <div style={{ 
          height: 32, 
          margin: 16, 
          background: 'rgba(255, 255, 255, 0.3)',
          borderRadius: 6,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontWeight: 'bold'
        }}>
          {collapsed ? 'DA' : 'District Admin'}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Sider>
      <AntLayout>
        <Header style={{ 
          padding: '0 16px', 
          background: '#fff', 
          display: 'flex', 
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{ fontSize: 16, width: 64, height: 64 }}
          />
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <span>Welcome, {user?.full_name || user?.username}</span>
            <Dropdown overlay={userMenu} placement="bottomRight">
              <Avatar icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
            </Dropdown>
          </div>
        </Header>
        <Content style={{ margin: '24px 16px', overflow: 'initial' }}>
          <div style={{ 
            padding: 24, 
            background: '#fff', 
            borderRadius: 6,
            minHeight: 360 
          }}>
            {children}
          </div>
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

// KPICard.js - Reusable KPI Card Component
import React from 'react';
import { Card, Statistic } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

const KPICard = ({ title, value, delta, suffix, precision = 0, color = '#1890ff' }) => {
  const isPositive = delta > 0;
  const deltaColor = isPositive ? '#52c41a' : '#f5222d';
  
  return (
    <Card>
      <Statistic
        title={title}
        value={value}
        precision={precision}
        valueStyle={{ color }}
        suffix={suffix}
      />
      {delta !== undefined && (
        <div style={{ marginTop: 8 }}>
          <Statistic
            value={Math.abs(delta)}
            precision={1}
            valueStyle={{ color: deltaColor, fontSize: 14 }}
            prefix={isPositive ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
            suffix="%"
          />
        </div>
      )}
    </Card>
  );
};

// TaskCard.js - Individual Task Card Component
import React from 'react';
import { Card, Tag, Button, Avatar, Space, Tooltip } from 'antd';
import { EditOutlined, ClockCircleOutlined, UserOutlined } from '@ant-design/icons';
import moment from 'moment';

const TaskCard = ({ task, onEdit, onStatusChange }) => {
  const getStatusColor = (status) => {
    const colors = {
      'Pending': 'orange',
      'In Progress': 'blue',
      'Completed': 'green',
      'Canceled': 'red'
    };
    return colors[status] || 'default';
  };

  const getPriorityColor = (priority) => {
    const colors = {
      'Low': 'green',
      'Medium': 'orange',
      'High': 'red',
      'Critical': 'purple'
    };
    return colors[priority] || 'default';
  };

  return (
    <Card
      size="small"
      title={task.task_name}
      extra={
        <Space>
          <Tag color={getPriorityColor(task.priority)}>{task.priority}</Tag>
          <Tag color={getStatusColor(task.status)}>{task.status}</Tag>
          <Button 
            type="text" 
            icon={<EditOutlined />} 
            onClick={() => onEdit(task)}
          />
        </Space>
      }
    >
      <p>{task.description}</p>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Space>
          <Avatar size="small" icon={<UserOutlined />} />
          <span style={{ fontSize: 12 }}>{task.assigned_to}</span>
        </Space>
        <Tooltip title="Due Date">
          <Space>
            <ClockCircleOutlined />
            <span style={{ fontSize: 12 }}>
              {moment(task.due_date).format('MMM DD, YYYY')}
            </span>
          </Space>
        </Tooltip>
      </div>
    </Card>
  );
};

export { LoginForm, Layout, KPICard, TaskCard };