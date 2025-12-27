// API类型定义

// 分页响应类型
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

// 用户相关类型
export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  role_id?: number;
  role?: { id: number; name: string; };
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  full_name?: string;
  is_active?: boolean;
  is_superuser?: boolean;
  role_id?: number;
}

export interface UserUpdate {
  username?: string;
  email?: string;
  password?: string;
  full_name?: string;
  is_active?: boolean;
  is_superuser?: boolean;
  role_id?: number;
}

// 角色相关类型
export interface Role {
  id: number;
  name: string;
  description?: string;
}

export interface RoleCreate {
  name: string;
  description?: string;
  permission_ids?: number[];
}

export interface RoleUpdate {
  name?: string;
  description?: string;
  permission_ids?: number[];
}

// 权限相关类型
export interface Permission {
  id: number;
  name: string;
  description?: string;
}

export interface PermissionCreate {
  name: string;
  description?: string;
}

export interface PermissionUpdate {
  name?: string;
  description?: string;
}

// 认证相关类型
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}