import React, { useState } from 'react';
import { Table, Button, Modal, Form, Input, message, Space, Popconfirm, Spin, Select } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { roleApi, permissionApi } from '../services/api';
import { Role, RoleCreate, RoleUpdate, Permission } from '../types/api';
import MainLayout from '../layouts/MainLayout';

const { Option } = Select;

const Roles: React.FC = () => {
  const [visible, setVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingRole, setEditingRole] = useState<Role | null>(null);
  const queryClient = useQueryClient();

  // 使用useQuery获取角色列表，配置缓存策略
  const { data: roles = [], isLoading: isRolesLoading, error: rolesError } = useQuery({
    queryKey: ['roles'],
    queryFn: () => roleApi.getRoles(),
    staleTime: 5 * 60 * 1000, // 5分钟内视为新鲜
    gcTime: 10 * 60 * 1000, // 10分钟后清理缓存
  });

  // 使用useQuery获取权限列表，配置缓存策略
  const { data: permissions = [], isLoading: isPermissionsLoading } = useQuery({
    queryKey: ['permissions'],
    queryFn: () => permissionApi.getPermissions(),
    staleTime: 5 * 60 * 1000, // 5分钟内视为新鲜
    gcTime: 10 * 60 * 1000, // 10分钟后清理缓存
  });

  // 使用useMutation创建角色
  const createRoleMutation = useMutation({
    mutationFn: (roleData: RoleCreate) => roleApi.createRole(roleData),
    onSuccess: () => {
      message.success('角色添加成功');
      setVisible(false);
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['roles'] });
    },
    onError: (error: any) => {
      message.error(error.message || '添加角色失败');
    },
  });

  // 使用useMutation更新角色
  const updateRoleMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: RoleUpdate }) => roleApi.updateRole(id, data),
    onSuccess: () => {
      message.success('角色更新成功');
      setVisible(false);
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['roles'] });
    },
    onError: (error: any) => {
      message.error(error.message || '更新角色失败');
    },
  });

  // 使用useMutation删除角色
  const deleteRoleMutation = useMutation({
    mutationFn: (id: number) => roleApi.deleteRole(id),
    onSuccess: () => {
      message.success('角色删除成功');
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['roles'] });
    },
    onError: (error: any) => {
      message.error(error.message || '删除角色失败');
    },
  });

  // 打开添加/编辑模态框
  const showModal = (role?: Role) => {
    if (role) {
      setEditingRole(role);
      form.setFieldsValue(role);
    } else {
      setEditingRole(null);
      form.resetFields();
    }
    setVisible(true);
  };

  // 关闭模态框
  const handleCancel = () => {
    setVisible(false);
  };

  // 保存角色（添加或编辑）
  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      if (editingRole) {
        // 编辑角色
        updateRoleMutation.mutate({ id: editingRole.id, data: values });
      } else {
        // 添加角色
        createRoleMutation.mutate(values);
      }
    } catch (error: any) {
      message.error(error.message || '保存角色失败');
    }
  };

  // 删除角色
  const handleDelete = (id: number) => {
    deleteRoleMutation.mutate(id);
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
      title: '角色名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: '操作',
      key: 'action',
      width: 180,
      render: (_: any, record: Role) => (
        <Space size="middle">
          <Button 
            type="link" 
            icon={<EditOutlined />} 
            onClick={() => showModal(record)}
            loading={updateRoleMutation.isPending}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个角色吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button 
              type="link" 
              danger 
              icon={<DeleteOutlined />}
              loading={deleteRoleMutation.isPending}
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
        <h2>角色管理</h2>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          onClick={() => showModal()}
          loading={createRoleMutation.isPending}
        >
          添加角色
        </Button>
      </div>
      
      {/* 加载状态 */}
      {isRolesLoading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <Spin size="large" />
        </div>
      ) : rolesError ? (
        <div style={{ color: 'red', textAlign: 'center', padding: '20px' }}>
          获取角色列表失败: {rolesError as string}
        </div>
      ) : (
        <Table
          columns={columns}
          dataSource={roles}
          loading={isRolesLoading}
          rowKey="id"
          pagination={{ 
            pageSize: 10, 
            showSizeChanger: true,
            showQuickJumper: true,
          }}
          scroll={{ x: 800 }} // 支持横向滚动，适应小屏幕
        />
      )}
      
      {/* 添加/编辑角色模态框 */}
      <Modal
        title={editingRole ? '编辑角色' : '添加角色'}
        open={visible}
        onOk={handleSave}
        onCancel={handleCancel}
        width={500}
        confirmLoading={createRoleMutation.isPending || updateRoleMutation.isPending}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="角色名称"
            rules={[{ required: true, message: '请输入角色名称!' }]}
          >
            <Input placeholder="请输入角色名称" />
          </Form.Item>
          
          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea placeholder="请输入角色描述" rows={3} />
          </Form.Item>
          
          <Form.Item
            name="permission_ids"
            label="权限"
            rules={[{ required: true, message: '请选择权限!' }]}
          >
            <Select
              mode="multiple"
              placeholder="请选择权限"
              loading={isPermissionsLoading}
              style={{ width: '100%' }}
            >
              {permissions.map(permission => (
                <Option key={permission.id} value={permission.id}>
                  {permission.name} - {permission.description}
                </Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </MainLayout>
  );
};

export default Roles;