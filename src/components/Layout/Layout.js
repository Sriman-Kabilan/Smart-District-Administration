import React, { useState } from 'react';
import { Layout as AntLayout, Menu, Avatar, Dropdown, Button } from 'antd';
import { 
  DashboardOutlined, 
  BarChartOutlined, 
  TeamOutlined,
  UnorderedListOutlined,
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
      icon: <UnorderedListOutlined />,
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

  const userMenu = {
    items: [
      {
        key: 'profile',
        icon: <UserOutlined />,
        label: 'Profile',
      },
      {
        type: 'divider',
      },
      {
        key: 'logout',
        icon: <LogoutOutlined />,
        label: 'Logout',
        onClick: handleLogout,
      },
    ],
  };

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider trigger={null} collapsible collapsed={collapsed}>
        <div className="sidebar-logo">
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
        <Header className="header-content">
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{ fontSize: 16, width: 64, height: 64 }}
          />
          <div className="user-info">
            <span>Welcome, {user?.full_name || user?.username}</span>
            <Dropdown menu={userMenu} placement="bottomRight">
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

export default Layout;