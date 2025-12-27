import React, { Suspense, lazy } from 'react';
import { ConfigProvider, Spin } from 'antd';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import zhCN from 'antd/locale/zh_CN';
import './App.css';

// 使用React.lazy实现组件懒加载，添加webpackChunkName注释，便于调试
const Login = lazy(() => import(/* webpackChunkName: "login" */ './pages/Login'));
const Dashboard = lazy(() => import(/* webpackChunkName: "dashboard" */ './pages/Dashboard'));
const Users = lazy(() => import(/* webpackChunkName: "users" */ './pages/Users'));
const Roles = lazy(() => import(/* webpackChunkName: "roles" */ './pages/Roles'));

// 创建QueryClient实例，优化缓存策略
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 10 * 60 * 1000, // 数据10分钟内视为新鲜，减少请求次数
      cacheTime: 30 * 60 * 1000, // 缓存30分钟，延长缓存时间
      refetchOnWindowFocus: false, // 窗口聚焦时不重新获取数据
      refetchOnReconnect: false, // 重新连接时不重新获取数据
      refetchOnMount: false, // 组件挂载时不重新获取数据
      retry: 1, // 失败时只重试1次，减少不必要的重试
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 10000), // 指数退避重试策略
    },
    mutations: {
      retry: 0, // 变更操作失败时不重试
    },
  },
  // 优化内存使用，限制缓存大小
  queryCache: {
    maxSize: 100, // 最多缓存100个查询结果
    gcTime: 60 * 60 * 1000, // 1小时后清理未使用的缓存
  },
});

// 检查是否已登录
const isAuthenticated = () => {
  return localStorage.getItem('token') !== null;
};

// 受保护的路由组件
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

// 创建路由配置
const router = createBrowserRouter([
  {
    path: '/login',
    element: (
      <Suspense 
        fallback={
          <div style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            height: '100vh' 
          }}>
            <Spin size="large" />
          </div>
        } 
      >
        <Login />
      </Suspense>
    ),
  },
  {
    path: '/',
    element: (
      <ProtectedRoute>
        <Suspense 
          fallback={
            <div style={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              height: '100vh' 
            }}>
              <Spin size="large" />
            </div>
          } 
        >
          <Dashboard />
        </Suspense>
      </ProtectedRoute>
    ),
  },
  {
    path: '/users',
    element: (
      <ProtectedRoute>
        <Suspense 
          fallback={
            <div style={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              height: '100vh' 
            }}>
              <Spin size="large" />
            </div>
          } 
        >
          <Users />
        </Suspense>
      </ProtectedRoute>
    ),
  },
  {
    path: '/roles',
    element: (
      <ProtectedRoute>
        <Suspense 
          fallback={
            <div style={{ 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center', 
              height: '100vh' 
            }}>
              <Spin size="large" />
            </div>
          } 
        >
          <Roles />
        </Suspense>
      </ProtectedRoute>
    ),
  },
  {
    path: '*',
    element: <Navigate to="/login" replace />,
  },
]);

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ConfigProvider>
  );
}

export default App;