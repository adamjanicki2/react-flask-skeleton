import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";
import path from "path";
import eslint from "vite-plugin-eslint";

export default defineConfig({
  plugins: [react(), svgr(), eslint({ lintOnStart: true })],
  resolve: {
    alias: {
      src: path.resolve(__dirname, "src"),
    },
  },
  build: {
    outDir: "build",
  },
  server: {
    port: 3000,
    proxy: {
      "/api/": { target: "http://localhost:8000", changeOrigin: true },
    },
  },
});
