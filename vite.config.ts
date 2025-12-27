import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { visualizer } from 'rollup-plugin-visualizer'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  return {
    plugins: [
      react(),
      // 仅在分析模式下启用可视化插件
      mode === 'analyze' && visualizer({
        open: true,
        gzipSize: true,
        brotliSize: true,
        filename: 'build/analyze/index.html'
      })
    ],
    server: {
      port: 3000,
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
        },
      },
    },
    build: {
      // 优化构建输出
      outDir: 'build',
      sourcemap: mode === 'development',
      // 优化CSS
      cssCodeSplit: true,
      // 优化静态资源
      assetsInlineLimit: 4096, // 4KB以下的资源内联
      // 优化代码分割
      rollupOptions: {
        output: {
          manualChunks: {
            'react-vendor': ['react', 'react-dom'],
            'antd': ['antd'],
            'react-query': ['@tanstack/react-query'],
            'router': ['react-router-dom'],
            'axios': ['axios'],
          }
        }
      }
    }
  }
})