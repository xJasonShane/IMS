import axios from 'axios';
import { 
  User, UserCreate, UserUpdate, 
  Role, RoleCreate, RoleUpdate, 
  Permission, PermissionCreate, PermissionUpdate,
  LoginRequest, LoginResponse
} from '../types/api';

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
  getUsers: (params?: { skip?: number; limit?: number }): Promise<User[]> => {
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
  getRoles: (params?: { skip?: number; limit?: number }): Promise<Role[]> => {
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
  getPermissions: (params?: { skip?: number; limit?: number }): Promise<Permission[]> => {
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