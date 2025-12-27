import React, { useState } from 'react';
import { Table, Button, Modal, Form, Input, message, Space, Popconfirm, Spin } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { userApi } from '../services/api';
import { User, UserCreate, UserUpdate } from '../types/api';
import MainLayout from '../layouts/MainLayout';

const Users: React.FC = () => {
  const [visible, setVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const queryClient = useQueryClient();

  // 使用useQuery获取用户列表，配置缓存策略
  const { data: users = [], isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => userApi.getUsers(),
    staleTime: 5 * 60 * 1000, // 5分钟内视为新鲜
    gcTime: 10 * 60 * 1000, // 10分钟后清理缓存
  });

  // 使用useMutation创建用户
  const createUserMutation = useMutation({
    mutationFn: (userData: UserCreate) => userApi.createUser(userData),
    onSuccess: () => {
      message.success('用户添加成功');
      setVisible(false);
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
    onError: (error: any) => {
      message.error(error.message || '添加用户失败');
    },
  });

  // 使用useMutation更新用户
  const updateUserMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: UserUpdate }) => userApi.updateUser(id, data),
    onSuccess: () => {
      message.success('用户更新成功');
      setVisible(false);
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
    onError: (error: any) => {
      message.error(error.message || '更新用户失败');
    },
  });

  // 使用useMutation删除用户
  const deleteUserMutation = useMutation({
    mutationFn: (id: number) => userApi.deleteUser(id),
    onSuccess: () => {
      message.success('用户删除成功');
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
    onError: (error: any) => {
      message.error(error.message || '删除用户失败');
    },
  });

  // 打开添加/编辑模态框
  const showModal = (user?: User) => {
    if (user) {
      setEditingUser(user);
      form.setFieldsValue(user);
    } else {
      setEditingUser(null);
      form.resetFields();
    }
    setVisible(true);
  };

  // 关闭模态框
  const handleCancel = () => {
    setVisible(false);
  };

  // 保存用户（添加或编辑）
  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      if (editingUser) {
        // 编辑用户
        updateUserMutation.mutate({ id: editingUser.id, data: values });
      } else {
        // 添加用户
        createUserMutation.mutate(values);
      }
    } catch (error: any) {
      message.error(error.message || '保存用户失败');
    }
  };

  // 删除用户
  const handleDelete = (id: number) => {
    deleteUserMutation.mutate(id);
  };

  // 表格列配置
  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 80,
    },
    {
      title: '用户名',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: '姓名',
      dataIndex: 'full_name',
      key: 'full_name',
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (isActive: boolean) => (
        <span>{isActive ? '启用' : '禁用'}</span>
      ),
      width: 100,
    },
    {
      title: '超级管理员',
      dataIndex: 'is_superuser',
      key: 'is_superuser',
      render: (isSuperuser: boolean) => (
        <span>{isSuperuser ? '是' : '否'}</span>
      ),
      width: 120,
    },
    {
      title: '操作',
      key: 'action',
      width: 180,
      render: (_: any, record: User) => (
        <Space size="middle">
          <Button 
            type="link" 
            icon={<EditOutlined />} 
            onClick={() => showModal(record)}
            loading={updateUserMutation.isPending}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个用户吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button 
              type="link" 
              danger 
              icon={<DeleteOutlined />}
              loading={deleteUserMutation.isPending}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <MainLayout>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <h2>用户管理</h2>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          onClick={() => showModal()}
          loading={createUserMutation.isPending}
        >
          添加用户
        </Button>
      </div>
      
      {/* 加载状态 */}
      {isLoading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <Spin size="large" />
        </div>
      ) : error ? (
        <div style={{ color: 'red', textAlign: 'center', padding: '20px' }}>
          获取用户列表失败: {error as string}
        </div>
      ) : (
        <Table
          columns={columns}
          dataSource={users}
          loading={isLoading}
          rowKey="id"
          pagination={{ 
            pageSize: 10, 
            showSizeChanger: true,
            showQuickJumper: true,
          }}
          scroll={{ x: 800 }} // 支持横向滚动，适应小屏幕
        />
      )}
      
      {/* 添加/编辑用户模态框 */}
      <Modal
        title={editingUser ? '编辑用户' : '添加用户'}
        open={visible}
        onOk={handleSave}
        onCancel={handleCancel}
        width={500}
        confirmLoading={createUserMutation.isPending || updateUserMutation.isPending}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="username"
            label="用户名"
            rules={[{ required: true, message: '请输入用户名!' }]}
          >
            <Input placeholder="请输入用户名" />
          </Form.Item>
          
          <Form.Item
            name="email"
            label="邮箱"
            rules={[
              { required: true, message: '请输入邮箱!' },
              { type: 'email', message: '请输入有效的邮箱地址!' }
            ]}
          >
            <Input placeholder="请输入邮箱" />
          </Form.Item>
          
          <Form.Item
            name="full_name"
            label="姓名"
          >
            <Input placeholder="请输入姓名" />
          </Form.Item>
          
          {!editingUser && (
            <Form.Item
              name="password"
              label="密码"
              rules={[{ required: true, message: '请输入密码!' }]}
            >
              <Input.Password placeholder="请输入密码" />
            </Form.Item>
          )}
          
          <Form.Item
            name="is_active"
            label="状态"
            valuePropName="checked"
          >
            <Input.Checkbox defaultChecked />
          </Form.Item>
          
          <Form.Item
            name="is_superuser"
            label="超级管理员"
            valuePropName="checked"
          >
            <Input.Checkbox />
          </Form.Item>
        </Form>
      </Modal>
    </MainLayout>
  );
};

export default Users;