import React, { useState } from 'react';
import { Table, Button, Modal, Form, Input, InputNumber, message, Space, Popconfirm, Spin } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { productApi } from '../services/api';
import { Product, ProductCreate, ProductUpdate } from '../types/api';
import MainLayout from '../layouts/MainLayout';

const Products: React.FC = () => {
  const [visible, setVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const queryClient = useQueryClient();

  // 分页状态
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  });

  // 使用useQuery获取商品列表，配置缓存策略和分页
  const { data: productsData = { items: [], total: 0 }, isLoading, error } = useQuery({
    queryKey: ['products', pagination.current, pagination.pageSize],
    queryFn: () => productApi.getProducts({ 
      skip: (pagination.current - 1) * pagination.pageSize, 
      limit: pagination.pageSize 
    }),
    staleTime: 5 * 60 * 1000, // 5分钟内视为新鲜
    gcTime: 10 * 60 * 1000, // 10分钟后清理缓存
  });

  // 分页变化处理
  const handlePaginationChange = (page: number, pageSize: number) => {
    setPagination(prev => ({
      ...prev,
      current: page,
      pageSize
    }));
  };

  // 提取商品列表和总数
  const products = productsData.items;
  const total = productsData.total;

  // 使用useMutation创建商品
  const createProductMutation = useMutation({
    mutationFn: (productData: ProductCreate) => productApi.createProduct(productData),
    onSuccess: () => {
      message.success('商品添加成功');
      setVisible(false);
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
    onError: (error: any) => {
      message.error(error.message || '添加商品失败');
    },
  });

  // 使用useMutation更新商品
  const updateProductMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ProductUpdate }) => productApi.updateProduct(id, data),
    onSuccess: () => {
      message.success('商品更新成功');
      setVisible(false);
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
    onError: (error: any) => {
      message.error(error.message || '更新商品失败');
    },
  });

  // 使用useMutation删除商品
  const deleteProductMutation = useMutation({
    mutationFn: (id: number) => productApi.deleteProduct(id),
    onSuccess: () => {
      message.success('商品删除成功');
      // 使相关查询失效，触发重新获取
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
    onError: (error: any) => {
      message.error(error.message || '删除商品失败');
    },
  });

  // 打开添加/编辑模态框
  const showModal = (product?: Product) => {
    if (product) {
      setEditingProduct(product);
      form.setFieldsValue(product);
    } else {
      setEditingProduct(null);
      form.resetFields();
    }
    setVisible(true);
  };

  // 关闭模态框
  const handleCancel = () => {
    setVisible(false);
  };

  // 保存商品（添加或编辑）
  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      if (editingProduct) {
        // 编辑商品
        updateProductMutation.mutate({ id: editingProduct.id, data: values });
      } else {
        // 添加商品
        createProductMutation.mutate(values);
      }
    } catch (error: any) {
      message.error(error.message || '保存商品失败');
    }
  };

  // 删除商品
  const handleDelete = (id: number) => {
    deleteProductMutation.mutate(id);
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
      title: '商品名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '商品编码',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: '类别',
      dataIndex: 'category',
      key: 'category',
      width: 120,
    },
    {
      title: '单位',
      dataIndex: 'unit',
      key: 'unit',
      width: 80,
    },
    {
      title: '价格',
      dataIndex: 'price',
      key: 'price',
      width: 100,
      render: (price: number) => `¥${price.toFixed(2)}`,
    },
    {
      title: '成本',
      dataIndex: 'cost',
      key: 'cost',
      width: 100,
      render: (cost: number) => `¥${cost.toFixed(2)}`,
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
      render: (_: any, record: Product) => (
        <Space size="middle">
          <Button 
            type="link" 
            icon={<EditOutlined />} 
            onClick={() => showModal(record)}
            loading={updateProductMutation.isPending}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个商品吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button 
              type="link" 
              danger 
              icon={<DeleteOutlined />}
              loading={deleteProductMutation.isPending}
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
        <h2>商品管理</h2>
        <Button 
          type="primary" 
          icon={<PlusOutlined />} 
          onClick={() => showModal()}
          loading={createProductMutation.isPending}
        >
          添加商品
        </Button>
      </div>
      
      {/* 加载状态 */}
      {isLoading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
          <Spin size="large" />
        </div>
      ) : error ? (
        <div style={{ color: 'red', textAlign: 'center', padding: '20px' }}>
          获取商品列表失败: {error as string}
        </div>
      ) : (
        <Table
          columns={columns}
          dataSource={products}
          loading={isLoading}
          rowKey="id"
          pagination={{
            current: pagination.current,
            pageSize: pagination.pageSize,
            total: total,
            showSizeChanger: true,
            showQuickJumper: true,
            pageSizeOptions: ['10', '20', '50', '100'],
            onChange: handlePaginationChange,
          }}
          scroll={{ x: 1200 }} // 支持横向滚动，适应小屏幕
        />
      )}
      
      {/* 添加/编辑商品模态框 */}
      <Modal
        title={editingProduct ? '编辑商品' : '添加商品'}
        open={visible}
        onOk={handleSave}
        onCancel={handleCancel}
        width={600}
        confirmLoading={createProductMutation.isPending || updateProductMutation.isPending}
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="name"
            label="商品名称"
            rules={[{ required: true, message: '请输入商品名称' }]}
          >
            <Input placeholder="请输入商品名称" />
          </Form.Item>

          <Form.Item
            name="code"
            label="商品编码"
            rules={[{ required: true, message: '请输入商品编码' }]}
          >
            <Input placeholder="请输入商品编码" />
          </Form.Item>

          <Form.Item
            name="category"
            label="商品类别"
          >
            <Input placeholder="请输入商品类别" />
          </Form.Item>

          <Form.Item
            name="unit"
            label="商品单位"
            initialValue="个"
          >
            <Input placeholder="请输入商品单位" />
          </Form.Item>

          <div style={{ display: 'flex', gap: 16 }}>
            <Form.Item
              name="price"
              label="商品价格"
              style={{ flex: 1 }}
              rules={[{ required: true, message: '请输入商品价格' }]}
            >
              <InputNumber
                style={{ width: '100%' }}
                placeholder="请输入商品价格"
                min={0}
                step={0.01}
              />
            </Form.Item>

            <Form.Item
              name="cost"
              label="商品成本"
              style={{ flex: 1 }}
              rules={[{ required: true, message: '请输入商品成本' }]}
            >
              <InputNumber
                style={{ width: '100%' }}
                placeholder="请输入商品成本"
                min={0}
                step={0.01}
              />
            </Form.Item>
          </div>

          <Form.Item
            name="description"
            label="商品描述"
          >
            <Input.TextArea
              placeholder="请输入商品描述"
              rows={4}
            />
          </Form.Item>
        </Form>
      </Modal>
    </MainLayout>
  );
};

export default Products;
