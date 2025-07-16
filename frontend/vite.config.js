import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
    cors: true,
    proxy: {
      // Proxy API requests to backend container
      '/move': 'http://backend:8000',
      '/ping': 'http://backend:8000',
      '/qtable': 'http://backend:8000',
    },
  },
});