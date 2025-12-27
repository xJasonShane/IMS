import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // 处理错误响应
    if (error.response?.status === 401) {
      // 未授权，清除token并跳转到登录页
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

// 用户API
export const userApi = {
  // 获取用户列表
  getUsers: (params?: { skip?: number; limit?: number }) => {
    return apiClient.get('/users', { params });
  },
  
  // 获取单个用户
  getUser: (id: number) => {
    return apiClient.get(`/users/${id}`);
  },
  
  // 创建用户
  createUser: (data: any) => {
    return apiClient.post('/users', data);
  },
  
  // 更新用户
  updateUser: (id: number, data: any) => {
    return apiClient.put(`/users/${id}`, data);
  },
  
  // 删除用户
  deleteUser: (id: number) => {
    return apiClient.delete(`/users/${id}`);
  },
};

// 角色API
export const roleApi = {
  // 获取角色列表
  getRoles: (params?: { skip?: number; limit?: number }) => {
    return apiClient.get('/roles', { params });
  },
  
  // 获取单个角色
  getRole: (id: number) => {
    return apiClient.get(`/roles/${id}`);
  },
  
  // 创建角色
  createRole: (data: any) => {
    return apiClient.post('/roles', data);
  },
  
  // 更新角色
  updateRole: (id: number, data: any) => {
    return apiClient.put(`/roles/${id}`, data);
  },
  
  // 删除角色
  deleteRole: (id: number) => {
    return apiClient.delete(`/roles/${id}`);
  },
};

// 权限API
export const permissionApi = {
  // 获取权限列表
  getPermissions: (params?: { skip?: number; limit?: number }) => {
    return apiClient.get('/permissions', { params });
  },
  
  // 获取单个权限
  getPermission: (id: number) => {
    return apiClient.get(`/permissions/${id}`);
  },
  
  // 创建权限
  createPermission: (data: any) => {
    return apiClient.post('/permissions', data);
  },
  
  // 更新权限
  updatePermission: (id: number, data: any) => {
    return apiClient.put(`/permissions/${id}`, data);
  },
  
  // 删除权限
  deletePermission: (id: number) => {
    return apiClient.delete(`/permissions/${id}`);
  },
};

// 登录API
export const authApi = {
  // 登录
  login: (data: { username: string; password: string }) => {
    return apiClient.post('/login', data);
  },
  
  // 登出
  logout: () => {
    localStorage.removeItem('token');
  },
};