import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, message, Space, Popconfirm, Select } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { roleApi, permissionApi } from '../services/api';
import MainLayout from '../layouts/MainLayout';

const { Option } = Select;

const Roles: React.FC = () => {
  const [roles, setRoles] = useState<any[]>([]);
  const [permissions, setPermissions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [visible, setVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingRole, setEditingRole] = useState<any>(null);

  // 获取角色列表
  const fetchRoles = async () => {
    setLoading(true);
    try {
      const data = await roleApi.getRoles();
      setRoles(data);
    } catch (error: any) {
      message.error(error.message || '获取角色列表失败');
    } finally {
      setLoading(false);
    }
  };

  // 获取权限列表
  const fetchPermissions = async () => {
    try {
      const data = await permissionApi.getPermissions();
      setPermissions(data);
    } catch (error: any) {
      message.error(error.message || '获取权限列表失败');
    }
  };

  // 组件挂载时获取数据
  useEffect(() => {
    fetchRoles();
    fetchPermissions();
  }, []);

  // 打开添加/编辑模态框
  const showModal = (role?: any) => {
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
        await roleApi.updateRole(editingRole.id, values);
        message.success('角色更新成功');
      } else {
        // 添加角色
        await roleApi.createRole(values);
        message.success('角色添加成功');
      }
      setVisible(false);
      fetchRoles(); // 刷新角色列表
    } catch (error: any) {
      message.error(error.message || '保存角色失败');
    }
  };

  // 删除角色
  const handleDelete = async (id: number) => {
    try {
      await roleApi.deleteRole(id);
      message.success('角色删除成功');
      fetchRoles(); // 刷新角色列表
    } catch (error: any) {
      message.error(error.message || '删除角色失败');
    }
  };

  // 表格列配置
  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
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
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button 
            type="link" 
            icon={<EditOutlined />} 
            onClick={() => showModal(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个角色吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
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
        >
          添加角色
        </Button>
      </div>
      
      <Table
        columns={columns}
        dataSource={roles}
        loading={loading}
        rowKey="id"
        pagination={{ pageSize: 10 }}
      />
      
      {/* 添加/编辑角色模态框 */}
      <Modal
        title={editingRole ? '编辑角色' : '添加角色'}
        open={visible}
        onOk={handleSave}
        onCancel={handleCancel}
        width={500}
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