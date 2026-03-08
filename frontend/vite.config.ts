import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})

// Для TypeScript
declare module 'vite' {
  interface ImportMetaEnv {
    readonly VITE_BOT_SUPPORT_USERNAME: string
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
}
