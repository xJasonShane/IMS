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

// 商品相关类型
export interface Product {
  id: number;
  name: string;
  code: string;
  description?: string;
  category?: string;
  unit: string;
  price: number;
  cost: number;
}

export interface ProductCreate {
  name: string;
  code: string;
  description?: string;
  category?: string;
  unit?: string;
  price?: number;
  cost?: number;
}

export interface ProductUpdate {
  name?: string;
  code?: string;
  description?: string;
  category?: string;
  unit?: string;
  price?: number;
  cost?: number;
}

// 仓库相关类型
export interface Warehouse {
  id: number;
  name: string;
  location?: string;
  description?: string;
}

export interface WarehouseCreate {
  name: string;
  location?: string;
  description?: string;
}

export interface WarehouseUpdate {
  name?: string;
  location?: string;
  description?: string;
}

// 库存相关类型
export interface Inventory {
  id: number;
  product_id: number;
  product: Product;
  quantity: number;
  warehouse_id?: number;
  warehouse?: Warehouse;
}

export interface InventoryCreate {
  product_id: number;
  quantity: number;
  warehouse_id?: number;
}

export interface InventoryUpdate {
  quantity?: number;
  warehouse_id?: number;
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