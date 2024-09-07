import { URL, fileURLToPath } from "node:url";
import vue from "@vitejs/plugin-vue";
import analyzer from "rollup-plugin-analyzer";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      src: fileURLToPath(new URL("src", import.meta.url)),
    },
  },
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => ["ion-icon"].includes(tag),
        },
      },
    }),
    analyzer({ summaryOnly: true }),
  ],
});
