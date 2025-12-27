import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';
import { 
  User, UserCreate, UserUpdate, 
  Role, RoleCreate, RoleUpdate, 
  Permission, PermissionCreate, PermissionUpdate,
  LoginRequest, LoginResponse
} from '../types/api';

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 15000, // 增加超时时间到15秒
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // 允许携带凭证
});

// 请求取消控制器，用于取消重复请求
const pendingRequests = new Map<string, AbortController>();

// 生成请求键
const generateRequestKey = (config: AxiosRequestConfig): string => {
  const { method, url, params, data } = config;
  return `${method}:${url}:${JSON.stringify(params)}:${JSON.stringify(data)}`;
};

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 取消重复请求
    const requestKey = generateRequestKey(config);
    if (pendingRequests.has(requestKey)) {
      const controller = pendingRequests.get(requestKey);
      controller?.abort();
      pendingRequests.delete(requestKey);
    }
    
    // 创建新的取消控制器
    const controller = new AbortController();
    config.signal = controller.signal;
    pendingRequests.set(requestKey, controller);
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // 移除已完成的请求
    const requestKey = generateRequestKey(response.config);
    pendingRequests.delete(requestKey);
    
    return response.data;
  },
  (error: AxiosError) => {
    // 移除已完成的请求
    if (error.config) {
      const requestKey = generateRequestKey(error.config);
      pendingRequests.delete(requestKey);
    }
    
    // 处理取消请求错误
    if (error.name === 'CanceledError') {
      return Promise.reject(new Error('请求已取消'));
    }
    
    // 处理网络错误
    if (!error.response) {
      return Promise.reject(new Error('网络错误，请检查网络连接'));
    }
    
    // 处理HTTP错误
    const status = error.response.status;
    const message = error.response.data?.message || '请求失败';
    
    // 处理401未授权错误
    if (status === 401) {
      // 未授权，清除token并跳转到登录页
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    
    // 处理429请求过多错误
    if (status === 429) {
      return Promise.reject(new Error('请求过于频繁，请稍后重试'));
    }
    
    // 处理500服务器错误
    if (status >= 500) {
      return Promise.reject(new Error('服务器错误，请稍后重试'));
    }
    
    return Promise.reject({ status, message });
  }
);

// 用户API
export const userApi = {
  // 获取用户列表
  getUsers: (params?: { skip?: number; limit?: number }): Promise<PaginatedResponse<User>> => {
    return apiClient.get('/users', { params });
  },
  
  // 获取单个用户
  getUser: (id: number): Promise<User> => {
    return apiClient.get(`/users/${id}`);
  },
  
  // 创建用户
  createUser: (data: UserCreate): Promise<User> => {
    return apiClient.post('/users', data);
  },
  
  // 更新用户
  updateUser: (id: number, data: UserUpdate): Promise<User> => {
    return apiClient.put(`/users/${id}`, data);
  },
  
  // 删除用户
  deleteUser: (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`/users/${id}`);
  },
};

// 角色API
export const roleApi = {
  // 获取角色列表
  getRoles: (params?: { skip?: number; limit?: number }): Promise<PaginatedResponse<Role>> => {
    return apiClient.get('/roles', { params });
  },
  
  // 获取单个角色
  getRole: (id: number): Promise<Role> => {
    return apiClient.get(`/roles/${id}`);
  },
  
  // 创建角色
  createRole: (data: RoleCreate): Promise<Role> => {
    return apiClient.post('/roles', data);
  },
  
  // 更新角色
  updateRole: (id: number, data: RoleUpdate): Promise<Role> => {
    return apiClient.put(`/roles/${id}`, data);
  },
  
  // 删除角色
  deleteRole: (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`/roles/${id}`);
  },
};

// 权限API
export const permissionApi = {
  // 获取权限列表
  getPermissions: (params?: { skip?: number; limit?: number }): Promise<PaginatedResponse<Permission>> => {
    return apiClient.get('/permissions', { params });
  },
  
  // 获取单个权限
  getPermission: (id: number): Promise<Permission> => {
    return apiClient.get(`/permissions/${id}`);
  },
  
  // 创建权限
  createPermission: (data: PermissionCreate): Promise<Permission> => {
    return apiClient.post('/permissions', data);
  },
  
  // 更新权限
  updatePermission: (id: number, data: PermissionUpdate): Promise<Permission> => {
    return apiClient.put(`/permissions/${id}`, data);
  },
  
  // 删除权限
  deletePermission: (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`/permissions/${id}`);
  },
};

// 商品API
export const productApi = {
  // 获取商品列表
  getProducts: (params?: { skip?: number; limit?: number }): Promise<PaginatedResponse<Product>> => {
    return apiClient.get('/products', { params });
  },
  
  // 获取单个商品
  getProduct: (id: number): Promise<Product> => {
    return apiClient.get(`/products/${id}`);
  },
  
  // 创建商品
  createProduct: (data: ProductCreate): Promise<Product> => {
    return apiClient.post('/products', data);
  },
  
  // 更新商品
  updateProduct: (id: number, data: ProductUpdate): Promise<Product> => {
    return apiClient.put(`/products/${id}`, data);
  },
  
  // 删除商品
  deleteProduct: (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`/products/${id}`);
  },
};

// 仓库API
export const warehouseApi = {
  // 获取仓库列表
  getWarehouses: (params?: { skip?: number; limit?: number }): Promise<PaginatedResponse<Warehouse>> => {
    return apiClient.get('/products/warehouses', { params });
  },
  
  // 获取单个仓库
  getWarehouse: (id: number): Promise<Warehouse> => {
    return apiClient.get(`/products/warehouses/${id}`);
  },
  
  // 创建仓库
  createWarehouse: (data: WarehouseCreate): Promise<Warehouse> => {
    return apiClient.post('/products/warehouses', data);
  },
  
  // 更新仓库
  updateWarehouse: (id: number, data: WarehouseUpdate): Promise<Warehouse> => {
    return apiClient.put(`/products/warehouses/${id}`, data);
  },
  
  // 删除仓库
  deleteWarehouse: (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`/products/warehouses/${id}`);
  },
};

// 库存API
export const inventoryApi = {
  // 获取库存列表
  getInventories: (params?: { skip?: number; limit?: number }): Promise<PaginatedResponse<Inventory>> => {
    return apiClient.get('/products/inventories', { params });
  },
  
  // 获取单个库存
  getInventory: (id: number): Promise<Inventory> => {
    return apiClient.get(`/products/inventories/${id}`);
  },
  
  // 创建库存
  createInventory: (data: InventoryCreate): Promise<Inventory> => {
    return apiClient.post('/products/inventories', data);
  },
  
  // 更新库存
  updateInventory: (id: number, data: InventoryUpdate): Promise<Inventory> => {
    return apiClient.put(`/products/inventories/${id}`, data);
  },
  
  // 删除库存
  deleteInventory: (id: number): Promise<{ message: string }> => {
    return apiClient.delete(`/products/inventories/${id}`);
  },
  
  // 商品入库
  inbound: (productId: number, quantity: number): Promise<Inventory> => {
    return apiClient.put(`/products/inventories/${productId}/inbound`, { quantity });
  },
  
  // 商品出库
  outbound: (productId: number, quantity: number): Promise<Inventory> => {
    return apiClient.put(`/products/inventories/${productId}/outbound`, { quantity });
  },
};

// 登录API
export const authApi = {
  // 登录
  login: (data: LoginRequest): Promise<LoginResponse> => {
    return apiClient.post('/auth/login', data);
  },
  
  // 登出
  logout: (): void => {
    localStorage.removeItem('token');
  },
};