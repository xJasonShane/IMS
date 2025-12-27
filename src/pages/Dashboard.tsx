import React from 'react';
import { Card, Statistic, Row, Col } from 'antd';
import { UserOutlined, TeamOutlined, DatabaseOutlined } from '@ant-design/icons';
import MainLayout from '../layouts/MainLayout';

const Dashboard: React.FC = () => {
  return (
    <MainLayout>
      <h2>仪表盘</h2>
      <Row gutter={16} style={{ marginTop: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="用户总数"
              value={0}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="角色总数"
              value={0}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="权限总数"
              value={0}
              prefix={<DatabaseOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>
      <Row gutter={16} style={{ marginTop: 24 }}>
        <Col span={24}>
          <Card title="系统概览" bordered={false}>
            <p>IMS仓库管理系统是一个功能强大的仓库管理解决方案，支持用户管理、角色管理、权限管理、商品管理、库存管理等核心功能。</p>
          </Card>
        </Col>
      </Row>
    </MainLayout>
  );
};

export default Dashboard;