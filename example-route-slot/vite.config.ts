// @ts-nocheck

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import viteBasicSslPlugin from '@vitejs/plugin-basic-ssl'

export default defineConfig({
    build: {
        outDir: 'panels/route-slot'
    },
    base: '/route-slot',
    server: {
        host: '0.0.0.0',
        https: false,
        port: 8084
    },
    resolve: {
        alias: {
            '@': '/src'
        }
    },
    plugins: [viteBasicSslPlugin(), vue()]
})
